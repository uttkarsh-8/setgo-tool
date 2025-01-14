import React, { useState } from 'react';

function App() {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [password, setPassword] = useState('');
    const [extractedMessage, setExtractedMessage] = useState('');

    const hideMessage = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('image', file);
        formData.append('message', message);
        formData.append('password', password);

        try {
            const response = await fetch('http://localhost:5000/hide', {
                method: 'POST',
                body: formData
            });
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'hidden_message.png';
            a.click();
        } catch (error) {
            alert('Error hiding message');
        }
    };

    const extractMessage = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('image', file);
        formData.append('password', password);

        try {
            const response = await fetch('http://localhost:5000/extract', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            setExtractedMessage(data.message);
        } catch (error) {
            alert('Error extracting message');
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '500px', margin: 'auto' }}>
            <h1>Steganography App</h1>
            
            <div style={{ marginBottom: '30px' }}>
                <h2>Hide Message</h2>
                <form onSubmit={hideMessage}>
                    <div>
                        <input 
                            type="file" 
                            onChange={(e) => setFile(e.target.files[0])} 
                            style={{ marginBottom: '10px' }}
                        />
                    </div>
                    <div>
                        <input 
                            type="text"
                            placeholder="Enter message" 
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            style={{ marginBottom: '10px', padding: '5px' }}
                        />
                    </div>
                    <div>
                        <input 
                            type="password"
                            placeholder="Enter password" 
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            style={{ marginBottom: '10px', padding: '5px' }}
                        />
                    </div>
                    <button type="submit" style={{ padding: '5px 10px' }}>Hide Message</button>
                </form>
            </div>

            <div>
                <h2>Extract Message</h2>
                <form onSubmit={extractMessage}>
                    <div>
                        <input 
                            type="file" 
                            onChange={(e) => setFile(e.target.files[0])}
                            style={{ marginBottom: '10px' }}
                        />
                    </div>
                    <div>
                        <input 
                            type="password"
                            placeholder="Enter password" 
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            style={{ marginBottom: '10px', padding: '5px' }}
                        />
                    </div>
                    <button type="submit" style={{ padding: '5px 10px' }}>Extract Message</button>
                </form>
                {extractedMessage && (
                    <div style={{ marginTop: '20px' }}>
                        <h3>Extracted Message:</h3>
                        <p>{extractedMessage}</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
