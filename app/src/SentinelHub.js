import React, { useState } from 'react';
import CreatorDashboard from './CreatorDashboard';
import LoginComponent from './LoginComponent';

const SentinelHub = () => {
    const [user, setUser] = useState(null);

    if (!user) {
        return <LoginComponent onLogin={setUser} />;
    }

    return <CreatorDashboard user={user} />;
};

export default SentinelHub;
