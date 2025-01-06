from openai import OpenAI

def summarize_document(content):
    """
    Summarize the document content using OpenAI GPT.
    """
    prompt = (
        "Summarize the content of the following document concisely, ensuring all critical points "
        "are retained. Avoid repetition, unnecessary details, and additional spaces. Present the "
        "summary in a structured manner suitable for use as a knowledge base for an AI agent to "
        "answer queries accurately and effectively.\n\n"
        f"Document:\n{content}"
    )
    client = OpenAI()
    response = client.chat.completions.create(
        model= "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a summarization assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def process_files(file_paths, output_file_path):
    """
    Read multiple markdown files, summarize their content, and write the output to a file.
    """
    combined_summary = ""

    for idx, file_path in enumerate(file_paths, start=1):
        with open(file_path, 'r') as file:
            content = file.read()
        summary = summarize_document(content)
        combined_summary += f"Summary of Document {idx}:\n{summary}\n\n"

    # Write to output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(combined_summary.strip())

    print(f"Summarized content written to {output_file_path}")
    
if __name__ == "__main__":
    file_paths = ["crustDataDE.md", "crustDataAPI.md", "DataDictionary.md"]  # Add as many file paths as needed
    output_file_path = "output_summary.md"

    process_files(file_paths, output_file_path)
