
import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)


def analyze_inquiries(df):
    results = []

    for index, row in df.iterrows():
        message = row["message"]

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You classify customer inquiries. "
                        "Return valid JSON with the fields: "
                        "category, priority, suggested_action. "
                        "Category must be Shipping, Billing, "
                        "Product, Refund, or Other. "
                        "Priority must be High, Medium, or Low. "
                        "Keep suggested_action to one short sentence. "
                        "Do not invent policies, discounts, or facts. "
                        "Suggest actions for the support team."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            response_format={"type": "json_object"}
        )

        result = json.loads(
            response.choices[0].message.content
        )

        results.append({
            "id": row["id"],
            "customer": row["customer"],
            "message": message,
            "category": result["category"],
            "priority": result["priority"],
            "suggested_action": result["suggested_action"]
        })

    return pd.DataFrame(results)
