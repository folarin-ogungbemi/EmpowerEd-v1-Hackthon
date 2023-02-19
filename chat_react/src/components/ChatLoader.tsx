import React from 'react'
import Spinner from 'react-bootstrap/Spinner';


export function ChatLoader() {
    return (
        <div className='d-flex justify-content-center mt-2'>
            <Spinner animation="border" variant="dark" role="status">
              <span className="visually-hidden">Loading...</span>
            </Spinner>
        </div>
        );
    }