import React from 'react';
import { useState, useEffect } from "react";
import {SyncLoader} from 'react-spinners';


function Answer(props) {
    const query = props.previousStep.message;
    console.log(query)
    const [message, setMessage] = useState("");
    const getAnswer = () => {
        fetch("http://127.0.0.1:5000",
        {
            method: "POST", 
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(query)
          }).then((response) => {return response.text()}).then((response) => setMessage(response));
    }

    useEffect(getAnswer, []);
    
    return (
        <div className="Answer">
            <p>
                {message?
                message:
                <div>
                    <SyncLoader 
                        size={5}
                        speedMultiplier = {0.6}
                        color = {'#000000'}
                     />
                </div>
                }
            </p>
        </div>
    );
}

export default Answer;