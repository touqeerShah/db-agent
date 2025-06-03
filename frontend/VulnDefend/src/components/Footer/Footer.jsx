import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLinkedinIn, faTwitter, faBehance } from '@fortawesome/free-brands-svg-icons';
import './Footer.css'; // Assuming you have some external CSS for additional styles

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="logo-section">
            <img 
              src="https://framerusercontent.com/images/20oeGq9SQ6t4N7faj9A9y5XjAg.png" 
              alt="Logo" 
              className="logo" 
            />
          </div>
          <div className="links-section">
            <a href="#hero">Overview</a>
            <a href="#features">Features</a>
            <a href="#references">References</a>
            <a href="#faq">Faq</a>
          </div>
          <div className="social-section">
            <a href="https://twitter.com" className="social-icon" aria-label="Twitter">
              <FontAwesomeIcon icon={faTwitter} />
            </a>
            <a href="https://linkedin.com" className="social-icon" aria-label="LinkedIn">
              <FontAwesomeIcon icon={faLinkedinIn} />
            </a>
            <a href="https://behance.net" className="social-icon" aria-label="Behance">
              <FontAwesomeIcon icon={faBehance} />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
