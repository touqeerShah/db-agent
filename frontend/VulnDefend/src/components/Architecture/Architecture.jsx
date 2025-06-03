import './Architecture.css'; // External CSS for styling
import llm_ggogle_project from '../../assets/llm-ggogle-project.svg';

const Architecture = () => {
  return (
    <section className="architecture-overview-section" data-framer-name="Overview" name="Overview">
      
      <div className="variant hidden">
        <div className="architecture-heading-container">
          <h2 className="architecture-heading-text">
            <span className="architecture-heading-gradient">Powerful Controls</span>
          </h2>
        </div>
      </div>

      <div className="variant hidden">
        <div className="architecture-description-container">
          <p className="architecture-description-text">
            Fuel your curiosity, expand your horizons, and achieve greatness by joining a vibrant community of learners.
          </p>
        </div>
      </div>


      <div className="architecture-image-wrapper">
        <img
          src={llm_ggogle_project}
          alt="A visual from the dashboard of Solaris"
          className="architecture-overview-image"
        />
      </div>
    </section>
  );
};

export default Architecture;
