import { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFacebookF, faLinkedinIn, faTwitter, faBehance } from "@fortawesome/free-brands-svg-icons";
import { faChevronLeft, faChevronRight } from "@fortawesome/free-solid-svg-icons";
import './Team.css'; // Assuming you place the provided CSS in this file
import touqeer from '../../assets/teams/touqeer.jpg'; // Import the image

const Team = () => {
    const teams = [
        {
            url: touqeer, // Directly assign the imported image here
            name: "Touqeer Abbas Shah",
            title: "Full Stack Developer",
            description: "Touqeer specializes in building modern web applications using the latest technologies.",
            facebook: "",
            linkedIn: "",
            twitter: "",
            email: ""
        },
        {
            url: "https://cdn.easyfrontend.com/pictures/team/team_8.png", // For external image URLs
            name: "Jane Doe",
            title: "Product Manager",
            description: "Jane has a passion for creating efficient workflows and improving product quality.",
            facebook: "",
            linkedIn: "",
            twitter: "",
            email: ""
        }
        // Add more team members here
    ];

    const [index, setIndex] = useState(0);
    const [team, setTeam] = useState(teams[0]);

    useEffect(() => {
        setTeam(teams[index]);
    }, [index]);

    const handlePrev = () => {
        setIndex((prevIndex) => (prevIndex === 0 ? teams.length - 1 : prevIndex - 1));
    };

    const handleNext = () => {
        setIndex((prevIndex) => (prevIndex === teams.length - 1 ? 0 : prevIndex + 1));
    };

    return (
        <>
            <div className="Team-header">
                <h2>Our Team</h2>
                <p>We see room for innovation beyond the industry giants. If you need more insightful reports, enhanced telemetry, or better workflows, let’s talk over lunch—our treat.</p>

                <section className="ezy__team8">
                    <div className="ezy__team8-list">
                        <div className="team-row">
                            {/* Image section */}
                            <div className="team-col team-image">
                                <div
                                    className="ezy__team8-bg-holder"
                                    style={{ backgroundImage: `url(${team?.url})` }} // Use template literals to handle dynamic URLs
                                />
                            </div>

                            {/* Content section */}
                            <div className="team-col team-content position-relative">
                                <div className="ezy__team8-content">
                                    <h1 className="mb-1">{team?.name}</h1>
                                    <p className="mb-4">{team?.title}</p>
                                    <p className="opacity-50 mb-0 ezy__team8-description">
                                        {team?.description}
                                    </p>

                                    {/* Social icons */}
                                    <div className="ezy__team8-social-links mt-4">
                                        <a href={team?.facebook} className="me-3">
                                            <FontAwesomeIcon icon={faFacebookF} />
                                        </a>
                                        <a href={team?.linkedIn} className="me-3">
                                            <FontAwesomeIcon icon={faLinkedinIn} />
                                        </a>
                                        <a href={team?.twitter} className="me-3">
                                            <FontAwesomeIcon icon={faTwitter} />
                                        </a>
                                        <a href="#">
                                            <FontAwesomeIcon icon={faBehance} />
                                        </a>
                                    </div>
                                </div>

                                {/* Navigation controls */}
                                <div className="ezy__team8-control">
                                    <button className="ezy__team8-control-prev me-3" onClick={handlePrev}>
                                        <FontAwesomeIcon icon={faChevronLeft} />
                                    </button>
                                    <div className="ezy__team8-number-shape">&nbsp;&nbsp;</div>
                                    <button className="ezy__team8-control-next" onClick={handleNext}>
                                        <FontAwesomeIcon icon={faChevronRight} />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </>
    );
};

export default Team;
