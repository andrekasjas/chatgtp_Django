from django.shortcuts import render
import openai
import os
from dotenv import load_dotenv
from django.views.decorators.clickjacking import xframe_options_exempt
load_dotenv()

@xframe_options_exempt
openai.api_key = os.path.join(os.environ.get('OPENAI_API_KEY'))
def chat(request):
    chat_history = request.session.get('chat_history', [])
    request.session['chat_history'] = chat_history
    if request.method == 'POST':
        message = request.POST.get('message')
        vacia = request.POST.get('vacia')
        if vacia:
            request.session['chat_history'] = []
        if message:
            chat_history.append({'user': message, 'bot': ''})

            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Conversación:\nUsuario: {message}\nAI:",
                temperature=0.5,
                max_tokens=100,
                n=1,
                stop=None,
                timeout=10,
            )
            answer = response.choices[0].text.strip()
            chat_history[-1]['bot'] = answer
    return render(request, 'chat.html', {'chat_history': chat_history})
