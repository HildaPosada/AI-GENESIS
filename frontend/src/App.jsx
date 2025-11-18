import { useState, useEffect } from 'react'

function App() {
  const [activeTab, setActiveTab] = useState('transaction')
  const [apiStatus, setApiStatus] = useState('checking')
  const [loading, setLoading] = useState(false)
  const [sampleType, setSampleType] = useState('normal')
  const [currentTransaction, setCurrentTransaction] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [apiBaseUrl, setApiBaseUrl] = useState('')

  useEffect(() => {
    // Auto-detect API URL for Codespaces/local
    const baseUrl = getApiBaseUrl()
    setApiBaseUrl(baseUrl)
    console.log('API Base URL:', baseUrl)
    checkHealth(baseUrl)
  }, [])

  const getApiBaseUrl = () => {
    // Check if we're in GitHub Codespaces
    const currentUrl = window.location.href
    if (currentUrl.includes('github.dev') || currentUrl.includes('githubpreview.dev')) {
      // Extract the base URL and replace port 3000 with 8000
      const url = new URL(currentUrl)
      const backendUrl = url.origin.replace('-3000.', '-8000.')
      return backendUrl
    }
    // Default to localhost for local development
    return 'http://localhost:8000'
  }

  const checkHealth = async (baseUrl) => {
    try {
      const response = await fetch(`${baseUrl}/api/health`)
      const data = await response.json()
      setApiStatus(data.status)
    } catch (error) {
      setApiStatus('offline')
      console.error('Health check failed:', error)
    }
  }

  const generateSampleTransaction = async () => {
    setLoading(true)
    setAnalysisResult(null)

    try {
      // Generate sample transaction
      const sampleResponse = await fetch(`${apiBaseUrl}/api/demo/generate-sample-transaction?fraud_type=${sampleType}`, {
        method: 'POST'
      })
      const transaction = await sampleResponse.json()
      setCurrentTransaction(transaction)

      // Analyze transaction
      const analysisResponse = await fetch(`${apiBaseUrl}/api/analyze/transaction`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(transaction)
      })
      const result = await analysisResponse.json()
      setAnalysisResult(result)

    } catch (error) {
      console.error('Analysis failed:', error)
      alert(`Analysis failed. Error: ${error.message}\n\nMake sure the backend is running and accessible at: ${apiBaseUrl}`)
    } finally {
      setLoading(false)
    }
  }

  const formatTechnologies = (tech) => {
    if (!tech) return null
    const icons = {
      'google_gemini': '🧠',
      'opus': '⚙️',
      'qdrant': '🔍',
      'aiml_api': '🤖'
    }
    return Object.entries(tech).map(([key, value]) => (
      <div key={key} className="mb-1">
        <strong>{icons[key] || '•'} {formatKey(key)}:</strong> {value}
      </div>
    ))
  }

  const formatKey = (key) => {
    return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-900 to-purple-900 shadow-lg">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">🛡️ AI Fraud Detection System</h1>
              <p className="text-blue-200 mt-1">AI Genesis Hackathon 2025 - Powered by 4 AI Technologies</p>
            </div>
            <div className="flex gap-4">
              <div className="text-right">
                <div className="text-sm text-blue-200">API Status</div>
                <div className="flex items-center gap-2 mt-1">
                  <div className={`w-3 h-3 rounded-full animate-pulse ${apiStatus === 'healthy' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <span className="font-semibold capitalize">{apiStatus}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Technology Stack Banner */}
      <div className="bg-gradient-to-r from-purple-800 to-pink-800 py-4">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-4 gap-4 text-center">
            <div className="flex flex-col items-center">
              <i className="fas fa-brain text-3xl mb-2"></i>
              <div className="font-semibold">Google Gemini</div>
              <div className="text-xs text-purple-200">Multimodal AI</div>
            </div>
            <div className="flex flex-col items-center">
              <i className="fas fa-cogs text-3xl mb-2"></i>
              <div className="font-semibold">Opus</div>
              <div className="text-xs text-purple-200">Workflow Automation</div>
            </div>
            <div className="flex flex-col items-center">
              <i className="fas fa-search text-3xl mb-2"></i>
              <div className="font-semibold">Qdrant</div>
              <div className="text-xs text-purple-200">Vector Search</div>
            </div>
            <div className="flex flex-col items-center">
              <i className="fas fa-robot text-3xl mb-2"></i>
              <div className="font-semibold">AI/ML API</div>
              <div className="text-xs text-purple-200">100+ Models</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-gray-700">
          <button
            onClick={() => setActiveTab('transaction')}
            className={`px-6 py-3 border-b-2 font-semibold transition ${activeTab === 'transaction' ? 'border-blue-500 text-blue-500' : 'border-transparent'}`}
          >
            <i className="fas fa-credit-card mr-2"></i>Transaction Analysis
          </button>
          <button
            onClick={() => setActiveTab('document')}
            className={`px-6 py-3 border-b-2 font-semibold transition ${activeTab === 'document' ? 'border-blue-500 text-blue-500' : 'border-transparent'}`}
          >
            <i className="fas fa-file-alt mr-2"></i>Document Analysis
          </button>
          <button
            onClick={() => setActiveTab('workflow')}
            className={`px-6 py-3 border-b-2 font-semibold transition ${activeTab === 'workflow' ? 'border-blue-500 text-blue-500' : 'border-transparent'}`}
          >
            <i className="fas fa-project-diagram mr-2"></i>Workflows
          </button>
        </div>

        {/* Transaction Analysis Tab */}
        {activeTab === 'transaction' && (
          <div className="space-y-6">
            <div className="grid grid-cols-3 gap-6">
              {/* Input Form */}
              <div className="col-span-1 bg-gray-800 rounded-lg p-6 shadow-xl">
                <h2 className="text-xl font-bold mb-4">Generate Sample Transaction</h2>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Transaction Type</label>
                    <select
                      value={sampleType}
                      onChange={(e) => setSampleType(e.target.value)}
                      className="w-full px-4 py-2 bg-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    >
                      <option value="normal">Normal Transaction</option>
                      <option value="suspicious">Suspicious Transaction</option>
                      <option value="fraud">Fraudulent Transaction</option>
                    </select>
                  </div>
                  <button
                    onClick={generateSampleTransaction}
                    disabled={loading}
                    className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-6 py-3 rounded-lg font-semibold transition"
                  >
                    {loading ? 'Analyzing...' : 'Generate & Analyze'}
                  </button>
                </div>
              </div>

              {/* Transaction Details */}
              <div className="col-span-2 bg-gray-800 rounded-lg p-6 shadow-xl">
                <h2 className="text-xl font-bold mb-4">Transaction Details</h2>
                {currentTransaction ? (
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <div className="text-sm text-gray-400">Transaction ID</div>
                        <div className="font-mono">{currentTransaction.transaction_id}</div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-400">Amount</div>
                        <div className="text-2xl font-bold text-green-400">${currentTransaction.amount}</div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-400">Merchant</div>
                        <div>{currentTransaction.merchant_name}</div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-400">Location</div>
                        <div>{currentTransaction.location}</div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-gray-500 py-8">
                    Generate a transaction to see details
                  </div>
                )}
              </div>
            </div>

            {/* Analysis Results */}
            {analysisResult && (
              <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
                <h2 className="text-2xl font-bold mb-4">
                  <i className="fas fa-shield-alt mr-2"></i>Fraud Analysis Results
                </h2>

                {/* Status Banner */}
                <div className={`border-l-4 p-4 mb-6 rounded ${analysisResult.is_fraudulent ? 'bg-red-900 border-red-500' : 'bg-green-900 border-green-500'}`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-2xl font-bold">
                        {analysisResult.is_fraudulent ? '⚠️ FRAUD DETECTED' : '✅ TRANSACTION APPROVED'}
                      </div>
                      <div className="mt-1">
                        Risk Level: <span className="uppercase font-bold">{analysisResult.risk_level}</span> |
                        Confidence: {(analysisResult.confidence_score * 100).toFixed(0)}%
                      </div>
                    </div>
                    <div className="text-5xl">
                      {analysisResult.is_fraudulent ? '🚨' : '🎉'}
                    </div>
                  </div>
                </div>

                {/* Technology Breakdown */}
                <div className="grid grid-cols-2 gap-6 mb-6">
                  <div className="bg-gray-700 rounded-lg p-4">
                    <h3 className="font-bold mb-3 text-blue-400">
                      <i className="fas fa-brain mr-2"></i>Technology Stack Used
                    </h3>
                    <div className="space-y-2 text-sm">
                      {formatTechnologies(analysisResult.analysis_details?.technologies_used)}
                    </div>
                  </div>
                  <div className="bg-gray-700 rounded-lg p-4">
                    <h3 className="font-bold mb-3 text-yellow-400">
                      <i className="fas fa-exclamation-triangle mr-2"></i>Risk Factors
                    </h3>
                    <ul className="space-y-1 text-sm">
                      {analysisResult.reasons?.map((reason, idx) => (
                        <li key={idx} className="flex items-start">
                          <span className="mr-2">•</span>
                          <span>{reason}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Similar Cases */}
                {analysisResult.similar_cases && analysisResult.similar_cases.length > 0 && (
                  <div className="bg-gray-700 rounded-lg p-4 mb-6">
                    <h3 className="font-bold mb-3 text-purple-400">
                      <i className="fas fa-search mr-2"></i>Similar Fraud Patterns Found (Qdrant)
                    </h3>
                    <div className="space-y-2">
                      {analysisResult.similar_cases.map((case_, idx) => (
                        <div key={idx} className="bg-gray-800 p-3 rounded flex justify-between items-center">
                          <div>
                            <div className="font-semibold">{case_.description}</div>
                            <div className="text-sm text-gray-400">
                              Type: {case_.type} | Severity: {case_.severity}
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-sm text-gray-400">Similarity</div>
                            <div className="text-xl font-bold text-blue-400">
                              {(case_.similarity_score * 100).toFixed(0)}%
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Recommended Actions */}
                <div className="bg-gray-700 rounded-lg p-4">
                  <h3 className="font-bold mb-3 text-red-400">
                    <i className="fas fa-tasks mr-2"></i>Recommended Actions
                  </h3>
                  <ul className="space-y-2">
                    {analysisResult.recommended_actions?.map((action, idx) => (
                      <li key={idx} className="flex items-center">
                        <input type="checkbox" className="mr-3 w-5 h-5" />
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Workflow Info */}
                {analysisResult.analysis_details?.workflow && (
                  <div className="bg-gradient-to-r from-purple-900 to-pink-900 rounded-lg p-4 mt-6">
                    <h3 className="font-bold mb-2 text-lg">
                      <i className="fas fa-cogs mr-2"></i>Automated Workflow Created (Opus)
                    </h3>
                    <div className="text-sm">
                      Workflow ID: <span className="font-mono">{analysisResult.analysis_details.workflow.workflow_id}</span>
                    </div>
                    <div className="text-sm mt-1">
                      Status: <span className="font-semibold">{analysisResult.analysis_details.workflow.status}</span>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Document Analysis Tab */}
        {activeTab === 'document' && (
          <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
            <h2 className="text-xl font-bold mb-4">Document Fraud Analysis</h2>
            <div className="text-center py-12 text-gray-400">
              <i className="fas fa-file-upload text-6xl mb-4"></i>
              <p>Upload invoices, bank statements, or ID documents</p>
              <p className="text-sm mt-2">Powered by Google Gemini Vision</p>
              <button className="mt-4 bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg">
                Upload Document
              </button>
            </div>
          </div>
        )}

        {/* Workflow Tab */}
        {activeTab === 'workflow' && (
          <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
            <h2 className="text-xl font-bold mb-4">Investigation Workflows</h2>
            <div className="text-center py-12 text-gray-400">
              <i className="fas fa-project-diagram text-6xl mb-4"></i>
              <p>Automated fraud investigation workflows</p>
              <p className="text-sm mt-2">Powered by Opus Workflow Automation</p>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 mt-12 py-6">
        <div className="container mx-auto px-6 text-center text-gray-400">
          <p>🏆 Built for AI Genesis Hackathon 2025</p>
          <p className="text-sm mt-2">Integrating Google Gemini, Opus, Qdrant, and AI/ML API</p>
        </div>
      </footer>
    </div>
  )
}

export default App
