import { useState, useEffect } from 'react'
import './App.css'

function App() {
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

  // Convert confidence score to risk score (0-100)
  const getRiskScore = () => {
    if (!analysisResult?.confidence_score) return 0
    return Math.round(analysisResult.confidence_score * 100)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">

      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass-card">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                <i className="fas fa-shield-alt text-white text-xl"></i>
              </div>
              <span className="text-xl font-bold gradient-text">FraudShield AI</span>
            </div>
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full pulse-glow ${apiStatus === 'healthy' ? 'bg-green-400' : 'bg-red-400'}`}></div>
                <span className="text-sm text-gray-300">
                  {apiStatus === 'healthy' ? 'All Systems Operational' : 'System Offline'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto text-center fade-in">
          <h1 className="text-6xl font-extrabold mb-6 leading-tight">
            Detect Fraud in <span className="gradient-text">Real-Time</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Powered by advanced AI models including Google Gemini, Opus, and Qdrant.
            Analyze transactions instantly with multi-model intelligence.
          </p>

          {/* Tech Stack Pills */}
          <div className="flex flex-wrap justify-center gap-3 mb-12">
            <div className="glass-card px-4 py-2 rounded-full text-sm flex items-center space-x-2">
              <i className="fas fa-brain text-purple-400"></i>
              <span>Google Gemini</span>
            </div>
            <div className="glass-card px-4 py-2 rounded-full text-sm flex items-center space-x-2">
              <i className="fas fa-cogs text-blue-400"></i>
              <span>Opus AI</span>
            </div>
            <div className="glass-card px-4 py-2 rounded-full text-sm flex items-center space-x-2">
              <i className="fas fa-database text-green-400"></i>
              <span>Qdrant</span>
            </div>
            <div className="glass-card px-4 py-2 rounded-full text-sm flex items-center space-x-2">
              <i className="fas fa-robot text-pink-400"></i>
              <span>AI/ML API</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 pb-20">
        <div className="grid lg:grid-cols-3 gap-8">

          {/* Control Panel */}
          <div className="lg:col-span-1">
            <div className="glass-card rounded-3xl p-8 hover-lift">
              <h2 className="text-2xl font-bold mb-6">Analyze Transaction</h2>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-3">Transaction Type</label>
                  <select
                    value={sampleType}
                    onChange={(e) => setSampleType(e.target.value)}
                    className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 transition text-white"
                  >
                    <option value="normal" className="bg-gray-800">✅ Normal Transaction</option>
                    <option value="suspicious" className="bg-gray-800">⚠️ Suspicious Activity</option>
                    <option value="fraud" className="bg-gray-800">🚨 Fraudulent</option>
                  </select>
                </div>

                <button
                  onClick={generateSampleTransaction}
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 disabled:scale-100"
                >
                  {loading ? (
                    <span className="flex items-center justify-center space-x-2">
                      <i className="fas fa-spinner fa-spin"></i>
                      <span>Analyzing...</span>
                    </span>
                  ) : (
                    <span className="flex items-center justify-center space-x-2">
                      <i className="fas fa-sparkles"></i>
                      <span>Generate & Analyze</span>
                    </span>
                  )}
                </button>
              </div>

              {/* Transaction Preview */}
              {currentTransaction && (
                <div className="mt-8 pt-8 border-t border-white/10">
                  <h3 className="text-lg font-semibold mb-4">Transaction Details</h3>
                  <div className="space-y-3 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Amount</span>
                      <span className="font-semibold">
                        ${currentTransaction.amount?.toFixed(2) || '-'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Type</span>
                      <span className="font-semibold">{currentTransaction.transaction_type || '-'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Merchant</span>
                      <span className="font-semibold">{currentTransaction.merchant_name || '-'}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2">
            {analysisResult && (
              <div className="glass-card rounded-3xl p-8 fade-in">

                {/* Risk Score Header */}
                <div className="mb-8">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-2xl font-bold">Analysis Results</h2>
                    <div className={`px-4 py-2 rounded-xl font-bold flex items-center space-x-2 ${
                      getRiskScore() < 30 ? 'bg-green-500/20 text-green-400' :
                      getRiskScore() < 70 ? 'bg-yellow-500/20 text-yellow-400' :
                      'bg-red-500/20 text-red-400'
                    }`}>
                      <span>{getRiskScore()}%</span>
                      <span>{analysisResult.is_fraudulent ? '🚨' : '✅'}</span>
                    </div>
                  </div>

                  {/* Risk Level Bar */}
                  <div className="relative h-3 bg-white/10 rounded-full overflow-hidden">
                    <div
                      style={{ width: `${getRiskScore()}%` }}
                      className={`h-full transition-all duration-1000 ease-out ${
                        getRiskScore() < 30 ? 'bg-gradient-to-r from-green-400 to-green-500' :
                        getRiskScore() < 70 ? 'bg-gradient-to-r from-yellow-400 to-orange-500' :
                        'bg-gradient-to-r from-red-400 to-red-600'
                      }`}
                    ></div>
                  </div>
                  <div className="flex justify-between text-xs text-gray-400 mt-2">
                    <span>Low Risk</span>
                    <span>High Risk</span>
                  </div>
                </div>

                {/* Risk Factors */}
                {analysisResult.reasons && analysisResult.reasons.length > 0 && (
                  <div className="mb-8">
                    <h3 className="text-lg font-semibold mb-4">Risk Factors</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {analysisResult.reasons.map((factor, index) => (
                        <div key={index} className="bg-white/5 rounded-xl p-4 border border-white/10">
                          <div className="text-sm text-gray-400 mb-1">Factor {index + 1}</div>
                          <div className="font-semibold">{factor}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* AI Insights */}
                <div className="mb-8">
                  <h3 className="text-lg font-semibold mb-4 flex items-center space-x-2">
                    <i className="fas fa-lightbulb text-yellow-400"></i>
                    <span>AI-Powered Insights</span>
                  </h3>
                  <div className="bg-purple-500/10 border border-purple-500/30 rounded-xl p-6">
                    <p className="text-gray-300 leading-relaxed">
                      {analysisResult.analysis_details?.explanation ||
                       `This transaction shows a ${analysisResult.risk_level} risk level with ${getRiskScore()}% confidence. ${analysisResult.is_fraudulent ? 'Fraudulent patterns detected.' : 'Transaction appears legitimate.'}`}
                    </p>
                  </div>
                </div>

                {/* Recommendations */}
                {analysisResult.recommended_actions && analysisResult.recommended_actions.length > 0 && (
                  <div className="mb-8">
                    <h3 className="text-lg font-semibold mb-4">Recommended Actions</h3>
                    <div className="space-y-3">
                      {analysisResult.recommended_actions.map((rec, index) => (
                        <div key={index} className="flex items-start space-x-3 bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
                          <i className="fas fa-check-circle text-blue-400 mt-1"></i>
                          <span className="text-gray-300">{rec}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Similar Cases from Qdrant */}
                {analysisResult.similar_cases && analysisResult.similar_cases.length > 0 && (
                  <div className="mb-8">
                    <h3 className="text-lg font-semibold mb-4 flex items-center space-x-2">
                      <i className="fas fa-search text-purple-400"></i>
                      <span>Similar Patterns (Qdrant)</span>
                    </h3>
                    <div className="space-y-3">
                      {analysisResult.similar_cases.slice(0, 3).map((case_, index) => (
                        <div key={index} className="bg-white/5 rounded-xl p-4 border border-white/10">
                          <div className="flex justify-between items-start">
                            <div>
                              <div className="font-semibold mb-1">{case_.description}</div>
                              <div className="text-sm text-gray-400">
                                Type: {case_.type} | Severity: {case_.severity}
                              </div>
                            </div>
                            <div className="text-right">
                              <div className="text-sm text-gray-400">Similarity</div>
                              <div className="text-xl font-bold text-purple-400">
                                {((case_.similarity_score || 0) * 100).toFixed(0)}%
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Technology Details */}
                <div className="mt-8 pt-8 border-t border-white/10">
                  <h3 className="text-sm font-semibold text-gray-400 mb-4">POWERED BY</h3>
                  <div className="grid grid-cols-4 gap-4">
                    <div className="text-center">
                      <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mx-auto mb-2">
                        <i className="fas fa-brain text-purple-400"></i>
                      </div>
                      <div className="text-xs text-gray-400">Gemini</div>
                    </div>
                    <div className="text-center">
                      <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center mx-auto mb-2">
                        <i className="fas fa-cogs text-blue-400"></i>
                      </div>
                      <div className="text-xs text-gray-400">Opus</div>
                    </div>
                    <div className="text-center">
                      <div className="w-12 h-12 bg-green-500/20 rounded-xl flex items-center justify-center mx-auto mb-2">
                        <i className="fas fa-database text-green-400"></i>
                      </div>
                      <div className="text-xs text-gray-400">Qdrant</div>
                    </div>
                    <div className="text-center">
                      <div className="w-12 h-12 bg-pink-500/20 rounded-xl flex items-center justify-center mx-auto mb-2">
                        <i className="fas fa-robot text-pink-400"></i>
                      </div>
                      <div className="text-xs text-gray-400">AI/ML API</div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Empty State */}
            {!analysisResult && (
              <div className="glass-card rounded-3xl p-16 text-center">
                <div className="w-24 h-24 bg-purple-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
                  <i className="fas fa-chart-line text-4xl text-purple-400"></i>
                </div>
                <h3 className="text-2xl font-bold mb-3">Ready to Analyze</h3>
                <p className="text-gray-400">
                  Select a transaction type and click "Generate & Analyze" to see AI-powered fraud detection in action.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-black/30 border-t border-white/10 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center space-x-2 text-gray-400 mb-2">
            <i className="fas fa-trophy text-yellow-400"></i>
            <span>Built for AI Genesis Hackathon 2025</span>
          </div>
          <p className="text-sm text-gray-500">
            Integrating Google Gemini · Opus · Qdrant · AI/ML API
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
