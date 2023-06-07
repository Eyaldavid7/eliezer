import React from 'react';
import { useState, useEffect } from "react";


function Answer() {
    const [message, setMessage] = useState("");

    const getAnswer = () => {
        fetch("http://127.0.0.1:5000").then((response) => {return response.text()}).then((response) => setMessage(response));
    }

    useEffect(getAnswer, []);
    
    return (
        <div className="Answer">
            <p>
                {message}
            </p>
        </div>
    );
}

export default Answer;