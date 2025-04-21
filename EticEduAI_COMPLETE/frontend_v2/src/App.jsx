import { useState } from "react"
import axios from "axios"

function App() {
  const [file, setFile] = useState(null)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [pdfUrl, setPdfUrl] = useState("")

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleUpload = async () => {
    if (!file) return alert("Selectează un fișier!")

    const formData = new FormData()
    formData.append("file", file)
    setLoading(true)

    try {
      const res = await axios.post("http://localhost:8000/verifica_licenta/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })

      setResults(res.data.rezultate)
      setPdfUrl(res.data.raport_pdf)
    } catch (err) {
      console.error(err)
      alert("Eroare la analiză.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f172a] to-[#1e293b] text-white p-10">
      <div className="max-w-4xl mx-auto bg-[#1e293b] p-8 rounded-2xl shadow-xl">
        <h1 className="text-3xl font-bold mb-4">EticEduAI</h1>
        <p className="mb-6 text-gray-300">Încarcă fișierul tău .docx/.pdf pentru analiză AI și plagiat.</p>
        <input
          type="file"
          onChange={handleFileChange}
          className="block w-full mb-4 text-sm text-gray-200 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
        />
        <button
          onClick={handleUpload}
          className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-xl font-semibold"
        >
          Trimite la analiză
        </button>
        {loading && <p className="mt-4">Se analizează...</p>}
        {results.length > 0 && (
          <div className="mt-8 space-y-6">
            {results.map((r, idx) => (
              <div key={idx} className="p-4 bg-gray-800 rounded-xl shadow">
                <p className="text-gray-300 text-sm mb-2">Paragraf: <span className="text-white">{r.paragraf}</span></p>
                <p className="text-green-400">Scor AI: {r.scor_ai}%</p>
                <p className="text-orange-400">Scor Plagiat: {r.scor_plagiat}%</p>
                <ul className="text-blue-300 text-sm mt-2">
                  {r.surse_similare.map((link, i) => (
                    <li key={i}><a href={link} target="_blank" rel="noopener noreferrer" className="underline">{link}</a></li>
                  ))}
                </ul>
              </div>
            ))}
            {pdfUrl && (
              <a href={pdfUrl} className="text-blue-500 underline block mt-6" target="_blank" rel="noreferrer">
                Descarcă raport PDF
              </a>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App