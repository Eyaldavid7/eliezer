import React from 'react';
import './App.css';
import ChatBot from 'react-simple-chatbot';
import { ThemeProvider } from 'styled-components';
import logo from './imgs/logo.png'
import Answer from './Answer.js';
 
// Creating our own theme
const theme = {
    background: '#C9FF8F',
    headerBgColor: '#197B22',
    headerFontSize: '20px',
    botBubbleColor: '#0F3789',
    headerFontColor: 'white',
    botFontColor: 'white',
    userBubbleColor: '#FF5733',
    userFontColor: 'white',
};
 
// Set some properties of the bot
const config = {
    floating: true,
    botAvatar: logo
};
 
function App() {

    const steps = [
        {
            id: 'bot_first_msg',
            message: 'Hey I\'m Eliezer, How can I help you?',
            trigger: 'user_question'
        }, {
            id: 'user_question',
     
            // This message appears in
            // the bot chat bubble
            user: true,
            trigger: 'bot_answer'
        },
        {
            id: 'bot_answer',
            
            // This message appears in
            // the bot chat bubble
            component: <Answer />,
            asMessage: true,
            trigger: 'user_question'
        }
    
    ]; 

    return (
        <div className="App">
                <ChatBot
 
                    // This appears as the header
                    // text for the chat bot
                    headerTitle="Eliezer"
                    steps={steps}
                    {...config}
                />
        </div>
    );
}
 
export default App;