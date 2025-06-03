// import React from 'react';
import './LunchFlow.css'; // Assuming this CSS is saved in LunchFlow.css
import agent from '../../assets/llm-lllm.svg';


const LunchFlow = () => {
    return (
        <>
            <div className="lunchflow-container">

                <div className="lunchflow-header">
                    <h2>Your Thoughts,<br /><span>Our Lunch</span></h2>
                    <p>We see room for innovation beyond the industry giants. If you need more insightful reports, enhanced telemetry, or better workflows, let’s talk over lunch—our treat.</p>
                </div>

                <div className="lunchflow-cards">
                    <div className="lunchflow-card ">
                        <h5>Complete employment authentication</h5>
                        <img src={agent}
                            alt="Complete workforce identity"
                            className="lunchflow-overview-image" />
                    </div>

               
                    <div className="lunchflow-card">
                        <h5>Identity automated processes</h5>
                        <img src="https://framerusercontent.com/images/ioKlvwW9068HDpFOPhgMSxQSOn4.png" alt="Identity automations" />
                    </div>
                </div>
            </div>

        </>
    );
};

export default LunchFlow;
