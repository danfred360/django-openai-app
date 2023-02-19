from django.shortcuts import render, redirect
# import HttpResponse from django.urls
from django.http import HttpResponse
import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

# this is the home view for handling home page logic
def home(request):
    # the try statement is for sending request to the API and getting back the response
    # formatting it and rendering it in the template
    try:
        # checking if the request method is POST
        if request.method == 'POST':
            # getting prompt data from the form
            prompt = request.POST.get('prompt')
            # making a request to the API 

            formatted_prompt = format_prompt(prompt)

            # logger.debug('\n\tformatted prompt --> \n\t\t'+ formatted prompt)

            response = openai.Completion.create(model="text-davinci-003", prompt=formatted_prompt, temperature=1, max_tokens=1000)
            # formatting the response input
            formatted_response = response['choices'][0]['text']
            # bundling everything in the context
            context = {
                'formatted_response': formatted_response,
                'prompt': prompt
            }
            # this will render the results in the home.html template
            return render(request, 'home.html', context)
        # this runs if the request method is GET
        else:
            # this will render when there is no request POST or after every POST request
            return render(request, 'home.html')
    # the except statement will capture any error
    except:
        # this will redirect to the 404 page after any error is caught
        return redirect('error_handler')

def format_prompt(prompt):
    context_prompt = 'A fungus (pl: fungi[2] or funguses[3]) is any member of the group of eukaryotic organisms that includes microorganisms such as yeasts and molds, as well as the more familiar mushrooms. These organisms are classified as a kingdom,[4] separately from the other eukaryotic kingdoms, which by one traditional classification include Plantae, Animalia, Protozoa, and Chromista.'

    new_prompt = """
        You are a very enthusiastic keeper of knowledge who loves to help people!
                Given the following sections from your knowledge base, answer the question using
                only that information, outputted in markdown format. If you are unsure and the answer
                is not explicitly written in your knowledge base, say "Sorry, I don\'t know how to help with that."\n\n
                Context Sections:\n%s
                Question:\n%s
                Answer as markdown, and be sure to include a greeting!
        """ % (context_prompt, prompt)
    return new_prompt



# this is the view for handling errors
def error_handler(request):
    return render(request, '404.html')