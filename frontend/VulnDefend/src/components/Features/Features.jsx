import FeatureCard from './FeatureCard/FeatureCard';
import './Features.css'; // External CSS for the grid layout
import ai from '../../assets/features/26-AM-unscreen.gif';
import test from '../../assets/features/test.gif';
import report from '../../assets/features/report.gif';
import artificial from '../../assets/features/artificial.gif';
import secure from '../../assets/features/secure.gif';
import study from '../../assets/features/study.gif';

// Features Section Component
const Features = () => {
  const features = [
    {
      title: 'AI Model',
      description: 'Ensure data security with our privacy-centric approach to API management.',
      icon: ai,
      imgUrl: 'https://framerusercontent.com/images/m9K2orpiKTpyArFtPrdshgxB1Q.png',
      backgroundImgUrl: 'https://framerusercontent.com/images/IB4pBCXqXDrRPrzyAYVAOxIYwmk.png'
    },
    {
      title: 'Testing',
      description: 'Seamlessly adapt to your evolving API needs, ensuring efficiency at any scale.',
      icon: test,
      imgUrl: 'https://framerusercontent.com/images/m9K2orpiKTpyArFtPrdshgxB1Q.png',
      backgroundImgUrl: 'https://framerusercontent.com/images/tdYnGTJeJF929QIECyV7QuQQP8.png'
    },
    {
      title: 'Report Generations',
      description: 'Effortlessly transition with robust tools for smooth API migration processes.',
      icon: report,
      imgUrl: 'https://framerusercontent.com/images/m9K2orpiKTpyArFtPrdshgxB1Q.png',
      backgroundImgUrl: 'https://framerusercontent.com/images/YYZufOsaTDP8kRzuBHzBWf84nA.png'
    },
    {
      title: 'Code Review',
      description: 'Schedule recurring tasks effortlessly with our intuitive job management.',
      icon: artificial,
      imgUrl: 'https://framerusercontent.com/images/m9K2orpiKTpyArFtPrdshgxB1Q.png',
      backgroundImgUrl: 'https://framerusercontent.com/images/gs6Lao5K9GZWaQvC24QuKzVrIM.png'
    },
    {
      title: 'Security Issues',
      description: 'Streamline operations with seamless command line interface compatibility.',
      icon: secure,
      imgUrl: 'https://framerusercontent.com/images/m9K2orpiKTpyArFtPrdshgxB1Q.png',
      backgroundImgUrl: 'https://framerusercontent.com/images/6u3apyyGrZOA1Xqe19adppXaSl4.png'
    },
    {
      title: 'Learning',
      description: 'Unlock cutting-edge capabilities with our innovative experimental toolkit.',
      icon: study,
      imgUrl: 'https://framerusercontent.com/images/m9K2orpiKTpyArFtPrdshgxB1Q.png',
      backgroundImgUrl: 'https://framerusercontent.com/images/I3gyBSI8AdYR56vr0AnaEaMdFs.png'
    }
  ];

  return (
    <div className="features-section">
      <h2 className="features-title">Features</h2>
      <p className="features-description">
        Improve your API experience with privacy, scalability, migration tools, job management, CLI support, and cutting-edge experimental features.
      </p>
      <div className="features-grid">
        {features.map((feature, index) => (
          <FeatureCard key={index} {...feature} />
        ))}
      </div>
    </div>
  );
};

export default Features;
