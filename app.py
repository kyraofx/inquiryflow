
import os
import json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the API key
load_dotenv()

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# 2. Read customer inquiries
df = pd.read_csv("inquiries.csv")

print(f"Total inquiries: {len(df)}")

# 3. Create an empty list for results
results = []

# 4. Process each customer inquiry
for index, row in df.iterrows():

    customer = row["customer"]
    message = row["message"]

    # Send the message to the AI model
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
    "content": (
        "You classify customer inquiries. "
        "Return only valid JSON with these fields: "
        "category, priority, suggested_action. "
        "Category must be Shipping, Billing, "
        "Product, Refund, or Other. "
        "Priority must be High, Medium, or Low. "
        "Keep suggested_action to one short sentence. "
        "Do not invent company policies, discounts, or facts. "
        "Suggest actions for the support team, not replies to customers."
    )
            },
            {
                "role": "user",
                "content": message
            }
        ],
        response_format={"type": "json_object"}
    )

    # 5. Convert AI response from JSON text to Python dictionary
    result = json.loads(
        response.choices[0].message.content
    )

    # 6. Add customer information and AI results to our list
    results.append({
        "id": row["id"],
        "customer": customer,
        "message": message,
        "category": result["category"],
        "priority": result["priority"],
        "suggested_action": result["suggested_action"]
    })

# 7. Convert results into a table
results_df = pd.DataFrame(results)

# 8. Display the results
print(results_df.to_string(index=False))

# 9. Save results to CSV
results_df.to_csv("/Users/kyraofx/Desktop/ai-career/inquiryflow/results.csv", index=False)

print("\nDone! Results saved to results.csv")
