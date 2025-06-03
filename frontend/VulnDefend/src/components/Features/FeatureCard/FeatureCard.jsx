import './FeatureCard.css'; // External CSS file for styling
import PropTypes from 'prop-types';

const FeatureCard = ({ icon, title, description }) => {
  return (
    <div className="feature-card">
      <div className="feature-card-inner">
        {/* Front Side */}
        <div className="feature-card-front">
          <div className="feature-card-top">
            <div className="feature-icon-title-wrapper">
              <div className="feature-icon-wrapper">
                <img src={icon} alt={title} className="feature-icon" />
              </div>
              <h3>{title}</h3>
            </div>
          </div>
          <div className="feature-partition"></div>
          <div className="feature-text-container">
            <p>{description}</p>
          </div>
        </div>

        {/* Back Side */}
        <div className="feature-card-back">
          <p>More details about {title}</p>
          {/* Add any additional info you'd like on the back */}
        </div>
      </div>
    </div>
  );
};

FeatureCard.propTypes = {
  title: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
};

export default FeatureCard;
