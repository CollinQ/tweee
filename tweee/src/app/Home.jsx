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
    const [ dateError, setDateError ] = useState(false);
    const [ emptyError, setEmptyError ] = useState(false);
    const [ loadingState, setLoadingState ] = useState(false);
    const { tweetText, setTweetText } = useContext(MyContext);
    const { tweetDate, setTweetDate } = useContext(MyContext);
    const { tweets, setTweets } = useContext(MyContext);

    const validateDate = (date) => {
        return /^\d{4}-\d{2}-\d{2}$/.test(date); // Regex to check date format
    };

    const fetchTweets = async (text, date) => {
        //Test:
        // const test = await fetch('http://127.0.0.1/test');
        // console.log('test: ', test);
        // const poop = await test.json();
        // console.log('test.text: ', poop["message"]);
        // console.log('test-headers: ', test.headers.get('Content-Type'));

        const url = `https://4ba6-2600-8802-5105-2700-a4ff-3649-f009-e21.ngrok-free.app/find-similar?text=${encodeURIComponent(text)}&date=${encodeURIComponent(date)}`;
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',  // This is typically necessary for APIs expecting JSON data
                    'ngrok-skip-browser-warning': 'true'  // Custom header to skip ngrok browser warning
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP status code: ${response.status}`);
            }
            console.log('Response: ', response);
            const data = await response.json();
            console.log('Data received:', data);
            await setTweets(tweets => {
                return {...tweets, ...data};
            });
            await setNavigate(true);
            console.log('tweets: ', tweets["week_0"]);
            return;
        } catch (error) {
            console.error('Fetch error:', error.message);
        }
    }

    const handleClick = async () => {
        //console.log(tweetText, tweetDate);
        if (!validateDate(tweetDate)) {
            setDateError(true); // Stop the function if the date is incorrect
        } else {
            setDateError(false); // Reset error state if date is correct
        }

        if (tweetText === "") {
            setEmptyError(true);
        }
        else {
            setEmptyError(false);
        }

        if (!validateDate(tweetDate) || tweetText === "") {return}
        else {
            setLoadingState(true);
        }

        await fetchTweets(tweetText, tweetDate);

        console.log('tweets: ', tweets)
        
        if (tweetText !== "" && tweetDate !== "" && Object.keys(tweets).length !== 0) {
            setNavigate(true);
        }
    }

    if (navigate) {
        return <Navigate to="/search" />
    }

    return (
        <div className="dark min-h-screen flex justify-center items-center bg-background">
            <div className="flex flex-col justify-center items-center p-4 w-3/4"> 
                <h1 className="text-3xl font-extrabold tracking-tight lg:text-5xl text-accent-foreground text-center">
                    Tweee
                </h1>
                <ReactTypingEffect
                    text={["The New Age of Media Digestion"]}
                    className="text-2xl font-extrabold tracking-tight lg:text-2xl text-accent-foreground text-center" // text-center ensures the text is centered
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
                    <div className="m-4 w-full flex flex-row"> 
                        <Input className = "ml-2 mr-2 w-4/5"
                        type="tweet-link" 
                        placeholder="Paste Tweet Text..."
                        onChange={(e) => setTweetText(e.target.value)}
                        />
                        <Input className = "ml-2 mr-2 w-1/5"
                        type="tweet-link" 
                        placeholder="Date (YYYY-MM-DD)"
                        onChange={(e) => setTweetDate(e.target.value)}
                        />
                    </div>
                    {!loadingState && <div className="m-4">
                        <Button variant="inputMatch" onClick={handleClick}>Submit</Button>
                    </div>}
                    {loadingState && 
                    <div className="m-4">
                        <Button variant="inputMatch" disabled="true" onClick={handleClick}>Loading...</Button>
                    </div>}
                </div>
                {dateError && (
                    <p className="text-red-500">Date must be in YYYY-MM-DD format</p>
                )}
                {emptyError && (
                    <p className="text-red-500">Fields cannot be left empty</p>
                )}
            </div>
        </div>
    )
}
