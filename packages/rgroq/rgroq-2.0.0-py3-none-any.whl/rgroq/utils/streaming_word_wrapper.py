from rgroq import config, getStringWidth, wrapText
from rgroq.utils.tts_utils import TTSUtil
#import pygments
#from pygments.lexers.markup import MarkdownLexer
#from prompt_toolkit.formatted_text import PygmentsTokens
#from prompt_toolkit import print_formatted_text
from prompt_toolkit.keys import Keys
from prompt_toolkit.input import create_input
import asyncio, shutil, textwrap, re, time


class StreamingWordWrapper:

    def __init__(self):
        self.streaming_finished = False
        config.tempChunk = ""
        self.start_time = None
        self.tokens = {"prompt": 0, "completion": 0, "total": 0}

    def wrapStreamWords(self, answer, terminal_width):
        if " " in answer:
            if answer == " ":
                if self.lineWidth < terminal_width:
                    print(" ", end='', flush=True)
                    self.lineWidth += 1
            else:
                answers = answer.split(" ")
                for index, item in enumerate(answers):
                    isLastItem = (len(answers) - index == 1)
                    itemWidth = getStringWidth(item)
                    newLineWidth = (self.lineWidth + itemWidth) if isLastItem else (self.lineWidth + itemWidth + 1)
                    if isLastItem:
                        if newLineWidth > terminal_width:
                            print(f"\n{item}", end='', flush=True)
                            self.lineWidth = itemWidth
                        else:
                            print(item, end='', flush=True)
                            self.lineWidth += itemWidth
                    else:
                        if (newLineWidth - terminal_width) == 1:
                            print(f"{item}\n", end='', flush=True)
                            self.lineWidth = 0
                        elif newLineWidth > terminal_width:
                            print(f"\n{item} ", end='', flush=True)
                            self.lineWidth = itemWidth + 1
                        else:
                            print(f"{item} ", end='', flush=True)
                            self.lineWidth += (itemWidth + 1)
        else:
            answerWidth = getStringWidth(answer)
            newLineWidth = self.lineWidth + answerWidth
            if newLineWidth > terminal_width:
                print(f"\n{answer}", end='', flush=True)
                self.lineWidth = answerWidth
            else:
                print(answer, end='', flush=True)
                self.lineWidth += answerWidth

    def keyToStopStreaming(self, streaming_event):
        async def readKeys() -> None:
            done = False
            input = create_input()

            def keys_ready():
                nonlocal done
                for key_press in input.read_keys():
                    #print(key_press)
                    if key_press.key in (Keys.ControlQ, Keys.ControlZ):
                        print("\n")
                        done = True
                        streaming_event.set()

            with input.raw_mode():
                with input.attach(keys_ready):
                    while not done:
                        if self.streaming_finished:
                            break
                        await asyncio.sleep(0.1)

        asyncio.run(readKeys())

    def streamOutputs(self, streaming_event, completion, openai=False):
        terminal_width = shutil.get_terminal_size().columns
        config.new_chat_response = ""
        self.start_time = time.time()

        # Track if we've seen the first response chunk
        first_chunk = True

        def finishOutputs(wrapWords, chat_response, terminal_width=terminal_width):
            config.wrapWords = wrapWords
            # reset config.tempChunk
            config.tempChunk = ""
            print("" if config.llmInterface == "llamacpp" else "\n")
            # add chat response to messages
            if chat_response:
                config.new_chat_response = chat_response
            if hasattr(config, "currentMessages") and chat_response:
                config.currentMessages.append({"role": "assistant", "content": chat_response})
            # auto pager feature
            if hasattr(config, "pagerView"):
                config.pagerContent += wrapText(chat_response, terminal_width) if config.wrapWords else chat_response
                #self.addPagerContent = False
                if config.pagerView:
                    config.launchPager(config.pagerContent)
            # finishing
            if hasattr(config, "conversationStarted"):
                config.conversationStarted = True
            self.streaming_finished = True

            # Display Groq stats
            elapsed_time = time.time() - self.start_time
            tokens_per_sec = self.tokens["completion"] / elapsed_time if elapsed_time > 0 else 0
            
            print("\n" + "─" * terminal_width)
            print(f"Tokens - Prompt: {self.tokens['prompt']} | Completion: {self.tokens['completion']} | Total: {self.tokens['total']}")
            print(f"Speed: {tokens_per_sec:.1f} tokens/sec | Time: {elapsed_time:.2f}s")

        chat_response = ""
        self.lineWidth = 0
        blockStart = False
        wrapWords = config.wrapWords
        firstEvent = True
        for event in completion:
            if not streaming_event.is_set() and not self.streaming_finished:
                # Get usage stats from first chunk for Groq API
                if first_chunk and isinstance(event, dict):
                    first_chunk = False
                    if "usage" in event:
                        usage = event.get("usage", {})
                        self.tokens = {
                            "prompt": usage.get("prompt_tokens", 0),
                            "completion": usage.get("completion_tokens", 0),
                            "total": usage.get("total_tokens", 0)
                        }
                    elif "choices" in event and len(event["choices"]) > 0:
                        # Alternative location in response
                        choice = event["choices"][0]
                        if "usage" in choice:
                            usage = choice["usage"]
                            self.tokens = {
                                "prompt": usage.get("prompt_tokens", 0),
                                "completion": usage.get("completion_tokens", 0),
                                "total": usage.get("total_tokens", 0)
                            }

                # RETRIEVE THE TEXT FROM THE RESPONSE
                if openai:
                    # openai
                    # when open api key is invalid for some reasons, event response in string
                    answer = event if isinstance(event, str) else event.choices[0].delta.content
                elif isinstance(event, dict):
                    if "message" in event:
                        # ollama chat
                        answer = event["message"].get("content", "")
                    else:
                        # llama.cpp chat
                        answer = event["choices"][0]["delta"].get("content", "")
                else:
                    # vertex ai
                    answer = event.text
                # transform
                if hasattr(config, "outputTransformers"):
                    for transformer in config.outputTransformers:
                        answer = transformer(answer)
                # STREAM THE ANSWER
                if answer is not None:
                    if firstEvent:
                        firstEvent = False
                        answer = answer.lstrip()
                    # display the chunk
                    chat_response += answer
                    # word wrap
                    if answer in ("```", "``"):
                        blockStart = not blockStart
                        if blockStart:
                            config.wrapWords = False
                        else:
                            config.wrapWords = wrapWords
                    if config.wrapWords:
                        if "\n" in answer:
                            lines = answer.split("\n")
                            for index, line in enumerate(lines):
                                isLastLine = (len(lines) - index == 1)
                                self.wrapStreamWords(line, terminal_width)
                                if not isLastLine:
                                    print("\n", end='', flush=True)
                                    self.lineWidth = 0
                        else:
                            self.wrapStreamWords(answer, terminal_width)
                    else:
                        print(answer, end='', flush=True) # Print the response
                    # speak streaming words
                    self.readAnswer(answer)
                if isinstance(event, dict) and "usage" in event:
                    # Update token counts from Groq response
                    usage = event["usage"]
                    self.tokens["prompt"] = usage.get("prompt_tokens", 0)
                    self.tokens["completion"] = usage.get("completion_tokens", 0)
                    self.tokens["total"] = usage.get("total_tokens", 0)
            else:
                finishOutputs(wrapWords, chat_response)
                return None
        
        if config.ttsOutput and config.tempChunk:
            # read the final chunk
            TTSUtil.play(config.tempChunk)
        config.tempChunk = ""
        finishOutputs(wrapWords, chat_response)

    def readAnswer(self, answer):
        # read the chunk when there is a punctuation
        #if answer in string.punctuation and config.tempChunk:
        if re.search(config.tts_startReadPattern, answer) and config.tempChunk:
            # read words when there a punctuation
            chunk = config.tempChunk + answer
            # play with tts
            if config.ttsOutput:
                TTSUtil.play(re.sub(config.tts_doNotReadPattern, "", chunk))
            # reset config.tempChunk
            config.tempChunk = ""
        else:
            # append to a chunk for reading
            config.tempChunk += answer