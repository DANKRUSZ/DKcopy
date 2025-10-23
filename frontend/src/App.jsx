import { useState } from 'react';
import './App.css';

// Template cards based on content types
const TEMPLATES = [
  {
    id: 'landing-hero',
    icon: '🌟',
    title: 'Landing Page Hero',
    description: 'Create compelling hero sections that grab attention and convert visitors',
    value: 'Landing page hero',
    popular: true
  },
  {
    id: 'email-intro',
    icon: '📧',
    title: 'Email Intro',
    description: 'Hook readers with engaging email openings that get clicks',
    value: 'Email intro',
    popular: true
  },
  {
    id: 'email-subject',
    icon: '✉️',
    title: 'Email Subject Line',
    description: 'Write subject lines that increase open rates',
    value: 'Email subject line'
  },
  {
    id: 'social-post',
    icon: '📱',
    title: 'Social Media Post',
    description: 'Generate scroll-stopping social content for all platforms',
    value: 'Social media post',
    popular: true
  },
  {
    id: 'product-desc',
    icon: '📦',
    title: 'Product Description',
    description: 'Craft persuasive product descriptions that drive sales',
    value: 'Product description',
    popular: true
  },
  {
    id: 'blog-post',
    icon: '📝',
    title: 'Blog Post',
    description: 'Write engaging blog content that ranks and resonates',
    value: 'Blog post'
  },
  {
    id: 'ad-copy',
    icon: '💰',
    title: 'Ad Copy',
    description: 'Create high-converting ad copy for all platforms',
    value: 'Ad copy'
  },
  {
    id: 'video-script',
    icon: '🎬',
    title: 'Video Script',
    description: 'Write compelling scripts for video content',
    value: 'Video script'
  }
];

function App() {
  const [view, setView] = useState('gallery'); // 'gallery' or 'form'
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [formData, setFormData] = useState({
    productInfo: '',
    targetAudience: '',
    contentType: ''
  });
  const [generatedContent, setGeneratedContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    setFormData({ ...formData, contentType: template.value });
    setView('form');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setGeneratedContent('');

    try {
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setGeneratedContent(data.content);
      } else {
        setError(data.error || 'Something went wrong');
      }
    } catch (err) {
      setError('Failed to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleBackToGallery = () => {
    setView('gallery');
    setSelectedTemplate(null);
    setGeneratedContent('');
    setError('');
  };

  const filteredTemplates = TEMPLATES.filter(template =>
    template.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    template.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const popularTemplates = filteredTemplates.filter(t => t.popular);
  const otherTemplates = filteredTemplates.filter(t => !t.popular);

  return (
    <div className="app">
      {view === 'gallery' ? (
        <div className="gallery-view">
          <div className="gallery-header">
            <div className="header-content">
              <h1>DK Copy</h1>
              <p className="tagline">AI-Powered Copywriting Assistant</p>
            </div>
            <div className="search-bar">
              <span className="search-icon">🔍</span>
              <input
                type="text"
                placeholder="Search templates..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          <div className="templates-container">
            {popularTemplates.length > 0 && (
              <div className="template-section">
                <h2 className="section-title">
                  <span className="star-icon">⭐</span>
                  Popular Templates
                </h2>
                <div className="template-grid">
                  {popularTemplates.map((template) => (
                    <div
                      key={template.id}
                      className="template-card"
                      onClick={() => handleTemplateSelect(template)}
                    >
                      <div className="template-icon">{template.icon}</div>
                      <h3 className="template-title">{template.title}</h3>
                      <p className="template-description">{template.description}</p>
                      <button className="template-btn">Use Template →</button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {otherTemplates.length > 0 && (
              <div className="template-section">
                <h2 className="section-title">All Templates</h2>
                <div className="template-grid">
                  {otherTemplates.map((template) => (
                    <div
                      key={template.id}
                      className="template-card"
                      onClick={() => handleTemplateSelect(template)}
                    >
                      <div className="template-icon">{template.icon}</div>
                      <h3 className="template-title">{template.title}</h3>
                      <p className="template-description">{template.description}</p>
                      <button className="template-btn">Use Template →</button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {filteredTemplates.length === 0 && (
              <div className="no-results">
                <p>No templates found matching "{searchQuery}"</p>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="form-view">
          <div className="form-header">
            <button className="back-btn" onClick={handleBackToGallery}>
              ← Back to Templates
            </button>
            <div className="template-info">
              <span className="template-icon-small">{selectedTemplate?.icon}</span>
              <h2>{selectedTemplate?.title}</h2>
            </div>
          </div>

          <div className="form-container">
            <form onSubmit={handleSubmit} className="content-form">
              <div className="form-group">
                <label htmlFor="productInfo">
                  Product/Service Information
                  <span className="required">*</span>
                </label>
                <textarea
                  id="productInfo"
                  name="productInfo"
                  value={formData.productInfo}
                  onChange={handleInputChange}
                  placeholder="Describe your product or service..."
                  required
                  rows="4"
                />
              </div>

              <div className="form-group">
                <label htmlFor="targetAudience">
                  Target Audience
                  <span className="required">*</span>
                </label>
                <textarea
                  id="targetAudience"
                  name="targetAudience"
                  value={formData.targetAudience}
                  onChange={handleInputChange}
                  placeholder="Describe your target audience..."
                  required
                  rows="4"
                />
              </div>

              <button type="submit" className="generate-btn" disabled={loading}>
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Generating...
                  </>
                ) : (
                  <>✨ Generate Content</>
                )}
              </button>
            </form>

            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                {error}
              </div>
            )}

            {generatedContent && (
              <div className="result-container">
                <div className="result-header">
                  <h3>Generated Content</h3>
                  <button
                    className="copy-btn"
                    onClick={() => {
                      navigator.clipboard.writeText(generatedContent);
                      alert('Copied to clipboard!');
                    }}
                  >
                    📋 Copy
                  </button>
                </div>
                <div className="result-content">
                  {generatedContent}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;