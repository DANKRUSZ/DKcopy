import { useState } from 'react';
import './App.css';

// Template cards based on your content types
const TEMPLATES = [
  {
    id: 'landing-hero',
    icon: '🌟',
    title: 'Landing Page Hero',
    description: 'Create compelling hero sections that grab attention and convert visitors',
    value: 'Landing page hero'
  },
  {
    id: 'email-intro',
    icon: '📧',
    title: 'Email Intro',
    description: 'Hook readers with engaging email openings that get clicks',
    value: 'Email intro'
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
    value: 'Social media post'
  },
  {
    id: 'product-desc',
    icon: '📦',
    title: 'Product Description',
    description: 'Craft persuasive product descriptions that drive sales',
    value: 'Product description'
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
  },
  {
    id: 'other',
    icon: '✨',
    title: 'Other',
    description: 'Custom content type for your unique needs',
    value: 'Other'
  }
];

function App() {
  const [view, setView] = useState('gallery'); // 'gallery' or 'editor'
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [formData, setFormData] = useState({
    productInfo: '',
    targetAudience: '',
    contentType: ''
  });
  const [generatedContent, setGeneratedContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState({ show: false, message: '', type: '' });

  // Floating label states
  const [focusedFields, setFocusedFields] = useState({
    productInfo: false,
    targetAudience: false
  });

  const showToast = (message, type = 'success') => {
    setToast({ show: true, message, type });
    setTimeout(() => setToast({ show: false, message: '', type: '' }), 3000);
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    setFormData({ ...formData, contentType: template.value });
    setView('editor');
    showToast(`${template.title} template selected`, 'success');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
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
        showToast('Content generated successfully!', 'success');
      } else {
        showToast(data.error || 'Something went wrong', 'error');
      }
    } catch (err) {
      showToast('Failed to connect to the server', 'error');
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
    setFormData({
      productInfo: '',
      targetAudience: '',
      contentType: ''
    });
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedContent);
    showToast('Copied to clipboard!', 'success');
  };

  const handleFocus = (field) => {
    setFocusedFields({ ...focusedFields, [field]: true });
  };

  const handleBlur = (field, value) => {
    if (!value) {
      setFocusedFields({ ...focusedFields, [field]: false });
    }
  };

  return (
    <div className="app">
      {/* Toast Notification */}
      {toast.show && (
        <div className={`toast toast-${toast.type}`}>
          <span className="toast-icon">
            {toast.type === 'success' ? '✓' : '⚠'}
          </span>
          {toast.message}
        </div>
      )}

      {view === 'gallery' ? (
        <div className="gallery-view">
          <div className="gallery-header">
            <h1>DK Copy</h1>
            <p className="subtitle">AI-Powered Copywriting Assistant</p>
          </div>

          <div className="templates-container">
            <div className="template-grid">
              {TEMPLATES.map((template, index) => (
                <div
                  key={template.id}
                  className="template-card"
                  onClick={() => handleTemplateSelect(template)}
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <div className="template-icon">{template.icon}</div>
                  <h3 className="template-title">{template.title}</h3>
                  <p className="template-description">{template.description}</p>
                  <button className="template-btn">Use Template →</button>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <div className="editor-view">
          <div className="editor-header">
            <button className="back-button" onClick={handleBackToGallery}>
              ← Back to Templates
            </button>
            <div className="template-info">
              <span className="template-icon-small">{selectedTemplate?.icon}</span>
              <span className="template-name">{selectedTemplate?.title}</span>
            </div>
          </div>

          <div className="editor-content">
            <div className="editor-form">
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <div className="floating-label-wrapper">
                    <textarea
                      id="productInfo"
                      name="productInfo"
                      value={formData.productInfo}
                      onChange={handleInputChange}
                      onFocus={() => handleFocus('productInfo')}
                      onBlur={(e) => handleBlur('productInfo', e.target.value)}
                      required
                      rows="5"
                    />
                    <label
                      htmlFor="productInfo"
                      className={focusedFields.productInfo || formData.productInfo ? 'active' : ''}
                    >
                      Product/Service Information <span className="required">*</span>
                    </label>
                  </div>
                </div>

                <div className="form-group">
                  <div className="floating-label-wrapper">
                    <textarea
                      id="targetAudience"
                      name="targetAudience"
                      value={formData.targetAudience}
                      onChange={handleInputChange}
                      onFocus={() => handleFocus('targetAudience')}
                      onBlur={(e) => handleBlur('targetAudience', e.target.value)}
                      required
                      rows="5"
                    />
                    <label
                      htmlFor="targetAudience"
                      className={focusedFields.targetAudience || formData.targetAudience ? 'active' : ''}
                    >
                      Target Audience <span className="required">*</span>
                    </label>
                  </div>
                </div>

                <button type="submit" className="generate-button" disabled={loading}>
                  {loading ? (
                    <>
                      <span className="spinner"></span>
                      Generating...
                    </>
                  ) : (
                    <>✨ Generate Copy</>
                  )}
                </button>
              </form>
            </div>

            <div className="editor-preview">
              {loading ? (
                <div className="loading-skeleton">
                  <div className="skeleton-header"></div>
                  <div className="skeleton-line"></div>
                  <div className="skeleton-line"></div>
                  <div className="skeleton-line short"></div>
                  <div className="skeleton-line"></div>
                  <div className="skeleton-line short"></div>
                </div>
              ) : generatedContent ? (
                <div className="preview-result">
                  <div className="preview-header">
                    <h3>Generated Content</h3>
                    <div className="preview-actions">
                      <button className="action-btn copy-btn" onClick={handleCopy}>
                        📋 Copy
                      </button>
                      <button className="action-btn regenerate-btn" onClick={handleSubmit}>
                        🔄 Generate Another
                      </button>
                    </div>
                  </div>
                  <div className="preview-content">
                    {generatedContent}
                  </div>
                </div>
              ) : (
                <div className="preview-empty">
                  <div className="empty-icon">✨</div>
                  <h3>Ready to generate</h3>
                  <p>Fill in the form and click "Generate Copy" to see your content appear here</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;