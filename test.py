from transformers import BertTokenizer, BertForSequenceClassification

CATEGORIES = {

0: "Utilities",
1: "Health",
2: "Dining",
3: "Travel",
4: "Education",
5: "Subscription",
6: "Family",
7: "Food",
8: "Festivals",
9: "Culture",
10: "Apparel",
11: "Transportation",
12: "Investment",
13: "Shopping",
14: "Groceries",
15: "Documents",
16: "Grooming",
17: "Entertainment",
18: "Social Life",
19: "Beauty",
20: "Rent",
21: "Money transfer",
22: "Salary",
23: "Tourism",
24: "Household",
}


# Load the model
model_name = "kuro-08/bert-transaction-categorization"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Sample transaction description
transaction = "Transaction: Payment at Starbucks for coffee - Type: income/expense"
inputs = tokenizer(transaction, return_tensors="pt", truncation=True, padding=True)

# Predict the category
outputs = model(**inputs)
logits = outputs.logits
predicted_category = logits.argmax(-1).item()

print(f"Predicted category: {CATEGORIES[predicted_category]}")
