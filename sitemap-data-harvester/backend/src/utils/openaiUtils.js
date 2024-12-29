require('dotenv').config();
const { OpenAI } = require('openai');

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

async function generateCompanySummary(content) {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        {
          role: "system",
          content: "You are a business analyst who creates concise company summaries. Focus on the company's main services, value propositions, and key offerings."
        },
        {
          role: "user",
          content: `Please create a concise summary of this company based on the following content: ${content}`
        }
      ],
      max_tokens: 1000,
      temperature: 0.7
    });

    return response.choices[0].message.content;
  } catch (error) {
    throw new Error('Failed to generate summary: ' + error.message);
  }
}

module.exports = {
  generateCompanySummary
};
