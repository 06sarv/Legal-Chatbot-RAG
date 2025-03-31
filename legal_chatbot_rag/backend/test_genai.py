import google.generativeai as genai

genai.configure(api_key="AIzaSyDKiZI2ikH8avxkBmHbI2SBi0YL7lfS5kk")

model = genai.GenerativeModel("gemini-1.5-pro-001")
response = model.generate_content("Explain the importance of legal AI chatbots.")

print(response.text)
