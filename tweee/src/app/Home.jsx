import React from "react";
import ReactTypingEffect from 'react-typing-effect';
import { useState } from "react";
import '../styles/globals.css';
import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";
import { Navigate } from "react-router-dom";
import { MyContext } from "../MyContext";
import { useContext } from "react";

export default function Home () {

    const [ navigate, setNavigate ] = useState(false);
    const { tweetText, setTweetText } = useContext(MyContext);

    const handleClick = async () => {
        console.log(tweetText);
        if (tweetText !== "") {
            setNavigate(true);
        }
    }

    if (navigate) {
        return <Navigate to="/search" />
    }

    return (
        <div className="dark min-h-screen flex justify-center items-center bg-background">
            <div className="flex flex-col justify-center items-center p-4 w-3/4"> 
                <ReactTypingEffect
                    text={["The New Age of Media Digestion"]}
                    className="text-4xl font-extrabold tracking-tight lg:text-5xl text-accent-foreground text-center" // text-center ensures the text is centered
                    cursorRenderer={ cursor => <h1> {cursor} </h1> }
                    displayTextRenderer={(text, i) => {
                        return (
                            <h1>
                            {text.split('').map((char, i) => {
                                const key = `${i}`;
                                return (
                                <span
                                    key={key}
                                >{char}</span>
                                );
                            })}
                            </h1>
                        );
                    }}
                />
                <div className="flex mt-8 w-full items-center justify-center">
                    <div className="m-4 w-full"> 
                        <Input 
                        type="tweet-link" 
                        placeholder="Enter Tweet Link..."
                        onChange={(e) => setTweetText(e.target.value)}
                        />
                    </div>
                    <div className="m-4">
                        <Button variant="inputMatch" onClick={handleClick}>Submit</Button>
                    </div>
                </div>
            </div>
        </div>
    )
}
