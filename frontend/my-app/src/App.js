import React from 'react';
import './App.css';
import ChatBot from 'react-simple-chatbot';
import { ThemeProvider } from 'styled-components';
import logo from './imgs/logo.png'
import mcs_logo from './imgs/mcs_logo.png'
import Answer from './Answer.js';
import { height, padding } from '@mui/system';

// Creating our own theme
const theme = {
    background: '#FAEBD7',
    headerBgColor: '#FF8C00',
    headerFontSize: '2.5vh',
    botBubbleColor: 'white',
    headerFontColor: 'white',
    botFontColor: 'black',
    userBubbleColor: 'white',
    userFontColor: 'black'
};
 
const config = {
    botAvatar: logo,
};
 
function App() {

    const steps = [
        {
            id: 'bot_first_msg',
            message: 'שלום אני אליעזר, איך אוכל לעזור?',
            trigger: 'user_question',
        }, {
            id: 'user_question',
            user: true,
            trigger: 'bot_answer',
            placeholder: "הקלד שאלה...",
        },
        {
            id: 'bot_answer',
            component: <Answer/>,
            asMessage: true,
            trigger: 'user_question',
            placeholder: "מחפש תשובה...",
        }
    
    ]; 

    return (
        <div className="App">
            <ThemeProvider theme={theme}>
                <ChatBot
                    headerTitle={
                    <p style={{'padding-top':'1vh'}}>
                        <img src={mcs_logo} 
                            width='40vw' 
                            heigh='40vh'/>      Eliezer
                    </p>}
                    bubbleStyle={{ direction: "rtl" , fontSize: '3vh'}}
                    avatarStyle={{height:"7vh"}}
                    inputStyle={{direction: "rtl", fontSize: '2vh'}}
                    width="100vw"
                    height="100vh"
                    steps={steps}
                    {...config}
                />
            </ThemeProvider>
        </div>
    );
}
 
export default App;