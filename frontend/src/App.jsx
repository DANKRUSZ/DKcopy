import { useState } from 'react';
import './App.css';

// Use environment variable for API URL, fallback to localhost for development
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

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
    id: 'tweet',
    icon: '🐦',
    title: 'Tweet',
    description: 'Craft concise, engaging tweets within 280 characters',
    value: 'Tweet'
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
    id: 'blog-intro',
    icon: '✍️',
    title: 'Blog Intro',
    description: 'Hook readers with compelling blog introductions',
    value: 'Blog intro'
  },
  {
    id: 'google-ad',
    icon: '🔍',
    title: 'Google Ad',
    description: 'Create brief, punchy Google ad copy that converts',
    value: 'Google ad'
  },
  {
    id: 'facebook-ad',
    icon: '👥',
    title: 'Facebook Ad',
    description: 'Write engaging Facebook ad copy that stops the scroll',
    value: 'Facebook ad'
  },
  {
    id: 'ad-copy',
    icon: '💰',
    title: 'Ad Copy',
    description: 'Create high-converting ad copy for various platforms',
    value: 'Ad copy'
  },
  {
    id: 'sales-page',
    icon: '💼',
    title: 'Sales Page',
    description: 'Write persuasive long-form sales copy that converts',
    value: 'Sales page'
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
  const [view, setView] = useState('gallery');
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [formData, setFormData] = useState({
    content_type: '',
    content_type_other: '',
    audience: '',
    product_info: '',
    tone_of_voice: '',
    style: '',
    brand_sample: '',
    keywords: '',
    cta: true
  });
  const [generatedContent, setGeneratedContent] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState({ show: false, message: '', type: '' });
  const [focusedFields, setFocusedFields] = useState({});

  const showToast = (message, type = 'success') => {
    setToast({ show: true, message, type });
    setTimeout(() => setToast({ show: false, message: '', type: '' }), 3000);
  };

  const handleTemplateSelect = (template) => {
    setSelectedTemplate(template);
    setFormData({ 
      ...formData, 
      content_type: template.value,
      content_type_other: ''
    });
    setView('editor');
    showToast(`${template.title} template selected`, 'success');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setGeneratedContent('');
    setIsEditing(false);

    try {
      const keywords = formData.keywords 
        ? formData.keywords.split(',').map(k => k.trim()).filter(k => k)
        : null;

      const payload = {
        content_type: formData.content_type === 'Other' ? formData.content_type_other : formData.content_type,
        audience: formData.audience,
        product_info: formData.product_info,
        cta: formData.cta,
        tone_of_voice: formData.tone_of_voice || null,
        style: formData.style || null,
        brand_sample: formData.brand_sample || null,
        keywords: keywords
      };

      const response = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
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
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleBackToGallery = () => {
    setView('gallery');
    setSelectedTemplate(null);
    setGeneratedContent('');
    setIsEditing(false);
    setFormData({
      content_type: '',
      content_type_other: '',
      audience: '',
      product_info: '',
      tone_of_voice: '',
      style: '',
      brand_sample: '',
      keywords: '',
      cta: true
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

  const handleContentEdit = (e) => {
    setGeneratedContent(e.target.value);
  };

  return (
    <div className="app">
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
                {formData.content_type === 'Other' && (
                  <div className="form-group">
                    <div className="floating-label-wrapper">
                      <input
                        type="text"
                        id="content_type_other"
                        name="content_type_other"
                        value={formData.content_type_other}
                        onChange={handleInputChange}
                        onFocus={() => handleFocus('content_type_other')}
                        onBlur={(e) => handleBlur('content_type_other', e.target.value)}
                        required
                      />
                      <label
                        htmlFor="content_type_other"
                        className={focusedFields.content_type_other || formData.content_type_other ? 'active' : ''}
                      >
                        Specify Content Type <span className="required">*</span>
                      </label>
                    </div>
                  </div>
                )}

                <div className="form-group">
                  <div className="floating-label-wrapper">
                    <input
                      type="text"
                      id="audience"
                      name="audience"
                      value={formData.audience}
                      onChange={handleInputChange}
                      onFocus={() => handleFocus('audience')}
                      onBlur={(e) => handleBlur('audience', e.target.value)}
                      required
                    />
                    <label
                      htmlFor="audience"
                      className={focusedFields.audience || formData.audience ? 'active' : ''}
                    >
                      Target Audience <span className="required">*</span>
                    </label>
                  </div>
                </div>

                <div className="form-group">
                  <div className="floating-label-wrapper">
                    <textarea
                      id="product_info"
                      name="product_info"
                      value={formData.product_info}
                      onChange={handleInputChange}
                      onFocus={() => handleFocus('product_info')}
                      onBlur={(e) => handleBlur('product_info', e.target.value)}
                      required
                      rows="4"
                    />
                    <label
                      htmlFor="product_info"
                      className={focusedFields.product_info || formData.product_info ? 'active' : ''}
                    >
                      Product/Service Information <span className="required">*</span>
                    </label>
                  </div>
                </div>

                <div className="form-group">
                  <div className="floating-label-wrapper">
                    <input
                      type="text"
                      id="tone_of_voice"
                      name="tone_of_voice"
                      value={formData.tone_of_voice}
                      onChange={handleInputChange}
                      onFocus={() => handleFocus('tone_of_voice')}
                      onBlur={(e) => handleBlur('tone_of_voice', e.target.value)}
                    />
                    <label
                      htmlFor="tone_of_voice"
                      className={focusedFields.tone_of_voice || formData.tone_of_voice ? 'active' : ''}
                    >
                      Tone of Voice
                    </label>
                  </div>
                </div>

                <div className="form-group">
                  <div className="floating-label-wrapper">
                    <input
                      type="text"
                      id="style"
                      name="style"
                      value={formData.style}
                      onChange={handleInputChange}
                      onFocus={() => handleFocus('style')}
                      onBlur={(e) => handleBlur('style', e.target.value)}
                    />
                    <label
                      htmlFor="style"
                      className={focusedFields.style || formData.style ? 'active' : ''}
                    >
                      Style Controls
                    </label>
                  </div>
                </div>

                <div className="form-group">
                  <div className="floating-label-wrapper">
                    <textarea
                      id="brand_sample"
                      name="brand_sample"
                      value={formData.brand_sample}
                      onChange={handleInputChange}
                      onFocus={() => handleFocus('brand_sample')}
                      onBlur={(e) => handleBlur('brand_sample', e.target.value)}
                      rows="3"
                    />
                    <label
                      htmlFor="brand_sample"
                      className={focusedFields.brand_sample || formData.brand_sample ? 'active' : ''}
                    >
                      Brand Voice Sample
                    </label>
                  </div>
                </div>

                <div className="form-group">
                  <div className="floating-label-wrapper">
                    <input
                      type="text"
                      id="keywords"
                      name="keywords"
                      value={formData.keywords}
                      onChange={handleInputChange}
                      onFocus={() => handleFocus('keywords')}
                      onBlur={(e) => handleBlur('keywords', e.target.value)}
                    />
                    <label
                      htmlFor="keywords"
                      className={focusedFields.keywords || formData.keywords ? 'active' : ''}
                    >
                      Keywords (comma-separated)
                    </label>
                  </div>
                </div>

                <div className="form-group checkbox-group">
                  <input
                    type="checkbox"
                    id="cta"
                    name="cta"
                    checked={formData.cta}
                    onChange={handleInputChange}
                  />
                  <label htmlFor="cta">Include Call-to-Action</label>
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
                      <button 
                        className="action-btn edit-btn" 
                        onClick={() => setIsEditing(!isEditing)}
                      >
                        {isEditing ? '👁️ Preview' : '✏️ Edit'}
                      </button>
                      <button className="action-btn copy-btn" onClick={handleCopy}>
                        📋 Copy
                      </button>
                      <button className="action-btn regenerate-btn" onClick={handleSubmit}>
                        🔄 Regenerate
                      </button>
                    </div>
                  </div>
                  <div className="preview-content">
                    {isEditing ? (
                      <textarea
                        className="content-editor"
                        value={generatedContent}
                        onChange={handleContentEdit}
                        rows="15"
                      />
                    ) : (
                      <div className="content-display">{generatedContent}</div>
                    )}
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