// Function to handle sending a message
async function sendMessage() {
    const userInput = document.getElementById('chat-input').value; // Corrected 'id' for input
    const chatOutput = document.getElementById('chat-output');    // Corrected 'id' for chat area
  
    // Validate user input
    if (userInput.trim() === '') {
      alert('Please type a message.');
      return;
    }
  
    // Display the user's message
    const userMessage = document.createElement('p');
    userMessage.textContent = `You: ${userInput}`;
    userMessage.style.color = 'blue';
    chatOutput.appendChild(userMessage);
  
    // Send the message to the backend
    try {
      const response = await fetch('http://127.0.0.1:5000/response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput }),
      });
  
      const data = await response.json();
      const botMessage = document.createElement('p');
  
      // Display the bot's response or error message
      if (data.response) {
        botMessage.textContent = `Bot: ${data.response}`;
      } else {
        botMessage.textContent = 'Bot: Something went wrong.';
      }
  
      chatOutput.appendChild(botMessage);
    } catch (error) {
      const errorMessage = document.createElement('p');
      errorMessage.textContent = 'Error: Unable to connect to the server.';
      chatOutput.appendChild(errorMessage);
    }
  
    // Scroll to the bottom of the chat area
    chatOutput.scrollTop = chatOutput.scrollHeight;
  
    // Clear the input field
    document.getElementById('chat-input').value = '';
  }
  
  // Attach event listener to the "Send" button
  document.getElementById('send-btn').addEventListener('click', sendMessage);
  