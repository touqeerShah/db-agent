import { useEffect } from "react";
import './Tools.css';
import chroma from '../../assets/logos/chroma.svg';
import gemini from '../../assets/logos/gemini.png';
import lama from '../../assets/logos/lama.png';
import langgraph from '../../assets/logos/langgraph.svg';
import LlamaIndex from '../../assets/logos/LlamaIndex.png';
import mongo from '../../assets/logos/mongo.png';

const Tools = () => {
    useEffect(() => {
        const logosSlide = document.querySelector('.tools-slide');
        if (logosSlide) {
            const copy = logosSlide.cloneNode(true);
            logosSlide.parentNode.classList.add('double-slide');
            logosSlide.parentNode.appendChild(copy);
        }
    }, []);

    return (
        <div className="tools">
            <div className="tools-slide">
                <img src={chroma} alt="chroma" />
                <img src={gemini} alt="gemini" />
                <img src={lama} alt="lama" />
                <img src={langgraph} alt="langgraph" />
                <img src={LlamaIndex} alt="LlamaIndex" />
                <img src={mongo} alt="mongo" />
            </div>
        </div>
    );
};

export default Tools;
