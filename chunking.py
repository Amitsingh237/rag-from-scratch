
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# ==================================
# 1. PYTHON FUNCTIONS
# ==================================

def add(a, b):
    print(f"\n[PYTHON FUNCTION] Adding {a} + {b}")
    return a + b


def multiply(a, b):
    print(f"\n[PYTHON FUNCTION] Multiplying {a} * {b}")
    return a * b


# ==================================
# 2. AVAILABLE TOOLS
# ==================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]


# ==================================
# 3. FUNCTION MAPPING
# ==================================

available_functions = {
    "add": add,
    "multiply": multiply
}


# ==================================
# 4. CONVERSATION HISTORY
# ==================================

messages = []

print("\n========== AI ASSISTANT STARTED ==========")


# ==================================
# 5. CONTINUOUS CHAT
# ==================================

while True:

    user_input = input("\n\nYOU: ")

    if user_input.lower() == "exit":
        print("Assistant stopped.")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    print("\n[DEBUG] User message added:")
    print(messages[-1])


    # ==================================
    # 6. LLM / TOOL EXECUTION LOOP
    # ==================================

    while True:

        print("\n========== SENDING REQUEST TO LLM ==========")

        stream = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=tools,
            stream=True
        )

        tool_calls = {}
        final_content = ""

        print("\n[DEBUG] Receiving streaming chunks...\n")


        # ==================================
        # 7. STREAMING LOOP
        # ==================================

        for chunk in stream:

            delta = chunk.choices[0].delta

            print("\n[RAW DELTA]", delta)

            # Normal text
            if delta.content:

                final_content += delta.content

                print("[AI TEXT]", end=" ")
                print(delta.content, end="", flush=True)


            # Tool-call updates
            if delta.tool_calls:

                for tc in delta.tool_calls:

                    index = tc.index

                    print(f"\n[TOOL UPDATE] Index: {index}")

                    if index not in tool_calls:

                        tool_calls[index] = {
                            "id": "",
                            "name": "",
                            "arguments": ""
                        }

                    if tc.id:
                        tool_calls[index]["id"] = tc.id

                    if tc.function.name:
                        tool_calls[index]["name"] += tc.function.name

                    if tc.function.arguments:
                        tool_calls[index]["arguments"] += tc.function.arguments

                    print("[CURRENT TOOL DATA]")
                    print(tool_calls[index])


        # ==================================
        # 8. DISPLAY COMPLETE TOOL CALLS
        # ==================================

        print("\n\n========== STREAM FINISHED ==========")

        print("\n[COMPLETE TOOL CALLS]")
        print(json.dumps(tool_calls, indent=4))


        # No tool call means normal answer is complete
        if not tool_calls:

            messages.append({
                "role": "assistant",
                "content": final_content
            })

            print("\n[DEBUG] Normal assistant message saved.")

            break


        # ==================================
        # 9. APPEND ASSISTANT TOOL CALLS
        # ==================================

        assistant_tool_calls = []

        for index in sorted(tool_calls):

            tc = tool_calls[index]

            assistant_tool_calls.append({
                "id": tc["id"],
                "type": "function",
                "function": {
                    "name": tc["name"],
                    "arguments": tc["arguments"]
                }
            })

        messages.append({
            "role": "assistant",
            "content": final_content if final_content else None,
            "tool_calls": assistant_tool_calls
        })

        print("\n[DEBUG] ASSISTANT TOOL-CALL MESSAGE:")
        print(json.dumps(messages[-1], indent=4))


        # ==================================
        # 10. EXECUTE TOOLS
        # ==================================

        for index in sorted(tool_calls):

            tc = tool_calls[index]

            name = tc["name"]
            call_id = tc["id"]

            print(f"\n========== EXECUTING {name} ==========")

            arguments = json.loads(tc["arguments"])

            print("[PARSED ARGUMENTS]", arguments)
            print("[ARGUMENT TYPE]", type(arguments))

            if name in available_functions:

                result = available_functions[name](**arguments)

            else:

                result = "Unknown function"

            print("[TOOL RESULT]", result)


            # ==================================
            # 11. APPEND TOOL RESULT
            # ==================================

            messages.append({
                "role": "tool",
                "tool_call_id": call_id,
                "content": str(result)
            })

            print("\n[DEBUG] TOOL MESSAGE ADDED:")
            print(messages[-1])


        # ==================================
        # 12. SHOW UPDATED CONVERSATION
        # ==================================

        print("\n========== UPDATED MESSAGES ==========")

        print(json.dumps(messages, indent=4))


        # Inner while loop repeats:
        # Send tool results back to LLM


    print("\n\n========== TURN COMPLETED ==========")


print("\n========== FINAL CONVERSATION HISTORY ==========")
print(json.dumps(messages, indent=4))
