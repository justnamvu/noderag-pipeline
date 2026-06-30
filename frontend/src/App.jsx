function App() {
  return (
    <div className="flex h-screen bg-white text-gray-900">
      {/* Sidebar */}
      <aside className="w-72 shrink-0 border-r border-gray-200 flex flex-col">
        <div className="px-4 py-4 border-b border-gray-200">
          <h1 className="text-sm font-medium text-gray-900">NodeRAG</h1>
        </div>

        <div className="flex-1 overflow-y-auto px-3 py-3">
          <p className="text-xs text-gray-400 px-1">No documents yet</p>
        </div>
      </aside>

      {/* Main chat panel */}
      <main className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto px-6 py-6">
          <div className="h-full flex items-center justify-center">
            <p className="text-sm text-gray-400">
              Upload a document to get started
            </p>
          </div>
        </div>
        
        <div className="border-t border-gray-200 px-6 py-4">
          <div className="max-w-2xl mx-auto">
            <div className="flex items-center gap-2 border border-gray-300 rounded-xl px-4 py-3">
              <input 
                type="text"
                placeholder="Ask a question about your documents..."
                className="flex-1 text-sm outline-none placeholder:text-gray-400"
                disabled
              />
              <button
                disabled
                className="text-sm font-medium text-gray-300 cursor-not-allowed"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App