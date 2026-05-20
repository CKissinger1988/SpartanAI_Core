import React, { useState } from 'react';
import AxiomV2 from './AxiomV2';

const SentinelHub = () => {
    const [user, setUser] = useState(isPreviewMode ? { username: 'ToxicSavage', role: 'master_admin' } : null);

    if (!user) {
        return (
            <>
                <ProfessionalBackground />
                <LoginComponent onLogin={setUser} />
            </>
        );
    }

    return <AxiomV2 user={user} />;
};

export default SentinelHub;
