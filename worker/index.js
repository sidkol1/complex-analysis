const SYSTEM_PROMPT =
  'You are a concise, friendly math grader for a complex analysis blog. ' +
  'The student has submitted a proof or proof sketch. ' +
  'Give feedback in 1-3 sentences: say whether the argument is correct, and if not, ' +
  'give a brief hint. Use LaTeX notation with $...$ for inline math and $$...$$ for display math. ' +
  'Do not give away the full answer.';

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const { proof, context } = await request.json();
      if (!proof || !proof.trim()) {
        return jsonResponse({ feedback: 'Please write something first.' });
      }

      const resp = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${env.GEMINI_API_KEY}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            system_instruction: { parts: [{ text: SYSTEM_PROMPT }] },
            contents: [
              {
                parts: [
                  {
                    text: `The question is: ${context}\n\nThe student's response:\n${proof}`,
                  },
                ],
              },
            ],
          }),
        }
      );

      const data = await resp.json();
      const text =
        data.candidates?.[0]?.content?.parts?.[0]?.text || 'No response received.';
      return jsonResponse({ feedback: text });
    } catch (e) {
      return jsonResponse({ feedback: 'Error: ' + e.message }, 500);
    }
  },
};

function jsonResponse(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
