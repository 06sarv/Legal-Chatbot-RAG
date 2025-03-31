import google.generativeai as genai

genai.configure(api_key="AIzaSyDKiZI2ikH8avxkBmHbI2SBi0YL7lfS5kk")

models = genai.list_models()
for model in models:
    print(model.name, model.supported_generation_methods)
