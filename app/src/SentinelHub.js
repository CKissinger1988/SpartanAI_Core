import React, { useState } from 'react';
import AxiomV2 from './AxiomV2';
import LoginComponent from './LoginComponent';

const SentinelHub = () => {
    const [user, setUser] = useState(null);

    if (!user) {
        return <LoginComponent onLogin={setUser} />;
    }

    return <AxiomV2 user={user} />;
};

export default SentinelHub;
