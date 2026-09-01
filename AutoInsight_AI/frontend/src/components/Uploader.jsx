import React, { useCallback, useState } from 'react';
import { FiUploadCloud } from 'react-icons/fi';

export default function Uploader({ onUpload, isLoading, onDemo }) {
  const [dragActive, setDragActive] = useState(false);
  
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUpload(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
      <h3 className="panel-title">Data Source</h3>
      <div 
        className={`uploader-container ${dragActive ? 'drag-active animate-pulse-border' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-upload').click()}
      >
        <FiUploadCloud className="uploader-icon" />
        <p style={{ fontWeight: 500, fontSize: '1.1rem' }}>Drag & Drop your dataset here</p>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '8px' }}>Supports .csv, .xls, .xlsx</p>
        <input 
          id="file-upload" 
          type="file" 
          accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" 
          style={{ display: 'none' }} 
          onChange={handleChange}
        />
      </div>
      <button 
        className="btn-primary" 
        onClick={onDemo} 
        disabled={isLoading}
        style={{ background: 'white', color: 'var(--primary)', border: '1px solid var(--primary)', marginTop: '12px' }}
      >
        Load Demo Data
      </button>
    </div>
  );
}
