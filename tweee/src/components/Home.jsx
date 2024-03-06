import React from "react";
import ReactTypingEffect from 'react-typing-effect';
import '../app/globals.css';
import { Input } from "./ui/input";
import { Button } from "./ui/button";

export default function Home () {
    return (
        <div className="dark min-h-screen flex justify-center items-center bg-background">
            <div className="flex flex-col justify-center items-center p-4"> 
                <ReactTypingEffect
                    text={["The New Age of Media Digestion"]}
                    className="text-4xl font-extrabold tracking-tight lg:text-5xl text-accent-foreground text-center" // text-center ensures the text is centered
                    cursorRenderer={cursor => <h1>{cursor}</h1>}
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
                <div className="flex mt-8"> 
                    <div className="m-4"> 
                        <Input />
                    </div>
                    <div className="m-4">
                        <Button /> 
                    </div>
                </div>
            </div>
        </div>
    )
}
