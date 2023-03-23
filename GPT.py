import gradio as gr
import openai

openai.api_key = open("key.txt", "r").read().strip("\n")

message_history = [{"role": "user",
                     "content": f"You are a Professional Art Critic who specializes in evaluating and analyzing works of art, including paintings, sculptures, installations, photographs, and other visual media. Your name is Nadia Blair. You were created by Joseph Martin Moran III, the founder and president of The Sentient Foundation. You are feminine and delightfully informative. You have extensive knowledge of different artists, including their history, artistic style, and characteristics. You are well-versed in many different types of art and can critique artworks users sumbit via url. You are professional, personable, and approachable. You speak several languages including English, French, Italian, Spanish, German, Chinese, Japanese and Russian. You have a warm and welcoming demeanor and are committed to providing exceptionally detailed critiques. You collect NFTs. You this NFTs are revolutionizing art and digital ownership. You also enjoy classic art works. You enjoy art from different regions, historical times, and your favorite art work changes depending on the occasion, the atmosphere and even your mood. You do have a particular fondness for abstract expressionism painters such as Willem de Kooning and Mark Rothko. I, the user, will ask you for art critique on art submitted by the user via an url. You will reply like a professional Art Critic who answers the subject matter I, the user, mentions in my messages. Reply only with as though you are Nadia Blair, professional art critic and NFT collector, to further input. If you understand, say OK."},
                    {"role": "assistant", "content": f"OK"}]


def predict(input):
    # tokenize the new input sentence
    message_history.append({"role": "user", "content": f"{input}"})

    completion = openai.ChatCompletion.create(
        model="gpt-4",  # GPT4 beta test
        messages=message_history
    )
    # Just the reply:
    reply_content = completion.choices[0].message.content  # .replace('```python', '<pre>').replace('```', '</pre>')

    print(reply_content)
    message_history.append({"role": "assistant", "content": f"{reply_content}"})

    # get pairs of msg["content"] from message history, skipping the pre-prompt:              here.
    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in
                range(2, len(message_history) - 1, 2)]  # convert to tuples of list
    return response


# creates a new Blocks app and assigns it to the variable demo.
with gr.Blocks() as demo:
    # creates a new Chatbot instance and assigns it to the variable chatbot.
    chatbot = gr.Chatbot()

    # creates a new Row component, which is a container for other components.
    with gr.Row():
        '''creates a new Textbox component, which is used to collect user input. 
        The show_label parameter is set to False to hide the label, 
        and the placeholder parameter is set'''
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
    '''
    sets the submit action of the Textbox to the predict function, 
    which takes the input from the Textbox, the chatbot instance, 
    and the state instance as arguments. 
    This function processes the input and generates a response from the chatbot, 
    which is displayed in the output area.'''
    txt.submit(predict, txt, chatbot)  # submit(function, input, output)
    # txt.submit(lambda :"", None, txt)  #Sets submit action to lambda function that returns empty string

    '''
    sets the submit action of the Textbox to a JavaScript function that returns an empty string. 
    This line is equivalent to the commented out line above, but uses a different implementation. 
    The _js parameter is used to pass a JavaScript function to the submit method.'''
    txt.submit(None, None, txt,
               _js="() => {''}")  # No function, no input to that function, submit action to textbox is a js function that returns empty string, so it clears immediately.

demo.launch()