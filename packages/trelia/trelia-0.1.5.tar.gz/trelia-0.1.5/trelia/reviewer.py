import os
import google.generativeai as genai
import json


class CodeReviewer:
    def __init__(self, model_name: str = 'gemini-1.5-flash'):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel(model_name)

    def grade_code(self, task_description: str, resource_code: str, resource_role: str) -> dict:
        # Step 1: Ask Gemini to give only a rating
        prompt = (
            f"Task: {task_description}\n"
            f"Code:\n{resource_code}\n"
            f"Role: {resource_role}\n"
            "You are a strict code reviewer. Rate from 1 to 5 as 'Rating: x.x/5'. "
            "Judge based on correctness, completeness, and if the code aligns with the role. "
            "Only return the rating."
        )
        response = self.model.generate_content(prompt)
        print(response.text)

        result = response.text.strip()

        rating = "N/A"
        feedback = "Unable to rate"

        # Step 2: Extract the rating
        if "Rating:" in result:
            try:
                rating_start = result.find("Rating:") + len("Rating: ")
                rating_end = result.find("/5", rating_start)
                rating_value = float(result[rating_start:rating_end].strip())
                rating = str(rating_value)

                # Step 3: Decision based on rating
                if rating_value > 2:
                    feedback = "Accepted"
                else:
                    # Ask Gemini for feedback only
                    feedback_prompt = (
                        f"Task: {task_description}\n"
                        f"Code:\n{resource_code}\n"
                        f"Student Role: {resource_role}\n"
                        "Give 1-line feedback (max 15 characters) for improving this code."
                    )
                    feedback_response = self.model.generate_content(feedback_prompt)
                    feedback = feedback_response.text.strip()
            except Exception as e:
                feedback = f"Error: {str(e)}"

        return json.dumps({"rating": rating, "feedback": feedback})
