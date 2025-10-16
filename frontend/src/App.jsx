import { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    content_type: '',
    content_type_other: '',
    audience: '',
    product_info: '',
    cta: true,
    tone_of_voice: '',
    style: '',
    brand_sample: '',
    keywords: ''
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    // Process keywords
    const keywords = formData.keywords
      .split(',')
      .map(k => k.trim())
      .filter(k => k);

    const payload = {
      content_type: formData.content_type === 'Other' ? formData.content_type_other : formData.content_type,
      audience: formData.audience,
      product_info: formData.product_info,
      cta: formData.cta,
      tone_of_voice: formData.tone_of_voice || null,
      style: formData.style || null,
      brand_sample: formData.brand_sample || null,
      keywords: keywords.length > 0 ? keywords : null
    };

    try {
      const response = await fetch('https://dkcopy-production.up.railway.app/api/v1/copy/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to generate copy');
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      content_type: '',
      content_type_other: '',
      audience: '',
      product_info: '',
      cta: true,
      tone_of_voice: '',
      style: '',
      brand_sample: '',
      keywords: ''
    });
    setResult(null);
    setError('');
  };

  const handleCopy = async () => {
    if (result) {
      await navigator.clipboard.writeText(result.generated_copy);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>DK Copy</h1>
        <p className="subtitle">AI-Powered Copywriting Tool</p>
      </header>

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="content_type">
              Content Type <span className="required">*</span>
            </label>
            <select
              id="content_type"
              name="content_type"
              value={formData.content_type}
              onChange={handleChange}
              required
            >
              <option value="">Select content type...</option>
              <option value="Landing page hero">Landing Page Hero</option>
              <option value="Email subject line">Email Subject Line</option>
              <option value="Email intro">Email Intro</option>
              <option value="Social media post">Social Media Post</option>
              <option value="Product description">Product Description</option>
              <option value="Facebook ad">Facebook Ad</option>
              <option value="Google ad">Google Ad</option>
              <option value="Blog intro">Blog Intro</option>
              <option value="Website headline">Website Headline</option>
              <option value="Other">Other</option>
            </select>
          </div>

          {formData.content_type === 'Other' && (
            <div className="form-group">
              <label htmlFor="content_type_other">
                Specify Content Type <span className="required">*</span>
              </label>
              <input
                type="text"
                id="content_type_other"
                name="content_type_other"
                value={formData.content_type_other}
                onChange={handleChange}
                placeholder="e.g., Press release, Video script, Billboard copy"
                required
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="audience">
              Target Audience <span className="required">*</span>
            </label>
            <input
              type="text"
              id="audience"
              name="audience"
              value={formData.audience}
              onChange={handleChange}
              placeholder="e.g., busy freelancers, B2B marketers, small business owners"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="product_info">
              Product/Service Info <span className="required">*</span>
            </label>
            <textarea
              id="product_info"
              name="product_info"
              value={formData.product_info}
              onChange={handleChange}
              placeholder="Describe what you're selling and its key benefits..."
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="tone_of_voice">Tone of Voice</label>
            <input
              type="text"
              id="tone_of_voice"
              name="tone_of_voice"
              value={formData.tone_of_voice}
              onChange={handleChange}
              placeholder="e.g., professional, friendly, witty, urgent"
            />
          </div>

          <div className="form-group">
            <label htmlFor="style">Style Controls</label>
            <input
              type="text"
              id="style"
              name="style"
              value={formData.style}
              onChange={handleChange}
              placeholder="e.g., short sentences, include statistics, avoid jargon"
            />
          </div>

          <div className="form-group">
            <label htmlFor="brand_sample">Brand Voice Sample</label>
            <textarea
              id="brand_sample"
              name="brand_sample"
              value={formData.brand_sample}
              onChange={handleChange}
              placeholder="Paste an example of the brand's existing copy (optional, max 3000 chars)"
            />
          </div>

          <div className="form-group">
            <label htmlFor="keywords">Keywords (comma-separated)</label>
            <input
              type="text"
              id="keywords"
              name="keywords"
              value={formData.keywords}
              onChange={handleChange}
              placeholder="e.g., productivity, automation, AI tool"
            />
          </div>

          <div className="form-group">
            <div className="checkbox-group">
              <input
                type="checkbox"
                id="cta"
                name="cta"
                checked={formData.cta}
                onChange={handleChange}
              />
              <label htmlFor="cta">Include Call-to-Action</label>
            </div>
          </div>

          <div className="button-group">
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Generating...' : 'Generate Copy'}
            </button>
            <button type="button" className="btn-secondary" onClick={handleReset}>
              Reset Form
            </button>
          </div>

          {error && (
            <div className="error">
              Error: {error}
            </div>
          )}
        </form>
      </div>

      {loading && (
        <div className="card loading">
          <div className="spinner"></div>
          <p>Generating your copy with Claude...</p>
        </div>
      )}

      {result && (
        <div className="card result-section">
          <div className="result-header">
            <h2 className="result-title">Generated Copy</h2>
            <button className={`copy-button ${copied ? 'copied' : ''}`} onClick={handleCopy}>
              {copied ? 'Copied!' : 'Copy to Clipboard'}
            </button>
          </div>
          <div className="result-meta">
            <span>~{result.metadata.tokens_used} tokens</span>
            <span>Cost: ${result.metadata.estimated_cost}</span>
          </div>
          <div className="result-copy">{result.generated_copy}</div>
          <div>
            <strong style={{ color: '#2d5016' }}>Keywords:</strong>
            <div className="keywords">
              {result.keywords.map((keyword, index) => (
                <span key={index} className="keyword-tag">
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;