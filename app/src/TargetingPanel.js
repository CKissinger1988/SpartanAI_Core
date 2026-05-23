import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { Aim, Plus, Globe, Monitor, Crosshair } from 'lucide-react';

const Root = styled.div`
    display: flex;
    flex-direction: column;
    gap: 20px;
    height: 100%;
`;

const InputGroup = styled.div`
    display: flex;
    gap: 10px;
`;

const Input = styled.input`
    flex: 1;
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid ${props => props.theme.colors.border};
    color: ${props => props.theme.colors.text};
    padding: 15px 20px;
    border-radius: 12px;
    font-family: inherit;
    outline: none;
    font-size: 0.95rem;
    transition: 0.3s;
    min-height: 55px;

    &:focus {
        border-color: ${props => props.theme.colors.primary};
        background: #fff;
    }
`;

const AddButton = styled.button`
    background: ${props => props.theme.colors.primary};
    color: #fff;
    border: none;
    padding: 0 25px;
    border-radius: 12px;
    cursor: pointer;
    font-size: 0.8rem;
    font-weight: 800;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: 0.3s;
    min-height: 55px;

    &:hover {
        background: #0088CC;
        box-shadow: 0 5px 15px rgba(0, 170, 255, 0.2);
    }
`;

const TargetList = styled.div`
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    -webkit-overflow-scrolling: touch;
`;

const TargetItem = styled.div`
    background: #fff;
    border: 1px solid ${props => props.theme.colors.border}44;
    padding: 15px 20px;
    border-radius: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: 0.3s;

    &:hover {
        border-color: ${props => props.theme.colors.primary}44;
        background: #F8FAFC;
    }
`;

const TargetInfo = styled.div`
    display: flex;
    align-items: center;
    gap: 15px;
`;

const TypeTag = styled.div`
    background: ${props => props.type === 'IP' ? '#00AAFF11' : '#6366f111'};
    color: ${props => props.type === 'IP' ? '#00AAFF' : '#6366f1'};
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.65rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 1px;
`;

const TargetLabel = styled.div`
    font-size: 0.95rem;
    font-weight: 700;
    color: ${props => props.theme.colors.text};
`;

const SelectBtn = styled.button`
    background: transparent;
    border: 1px solid ${props => props.theme.colors.primary}44;
    color: ${props => props.theme.colors.primary};
    padding: 8px 15px;
    border-radius: 10px;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    cursor: pointer;
    transition: 0.3s;
    display: flex;
    align-items: center;
    gap: 6px;

    &:hover {
        background: ${props => props.theme.colors.primary};
        color: #fff;
    }
`;

const TargetingPanel = ({ onTargetSelect }) => {
    const [targets, setTargets] = useState([
        { id: '192.168.1.101', type: 'IP' },
        { id: 'scan-results.local', type: 'DOMAIN' }
    ]);
    const [inputValue, setInputValue] = useState('');

    const handleAddTarget = () => {
        if (!inputValue || targets.some(t => t.id === inputValue)) return;
        const type = /^[0-9.]+$/.test(inputValue) ? 'IP' : 'DOMAIN';
        setTargets([...targets, { id: inputValue, type }]);
        setInputValue('');
    };

    return (
        <Root>
            <InputGroup>
                <Input
                    placeholder="Enter IP or Domain..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleAddTarget()}
                />
                <AddButton onClick={handleAddTarget}>
                    <Plus size={18} />
                    Acquire
                </AddButton>
            </InputGroup>
            <TargetList>
                {targets.map((target, i) => (
                    <TargetItem key={i}>
                        <TargetInfo>
                            {target.type === 'IP' ? <Monitor size={18} opacity={0.5} /> : <Globe size={18} opacity={0.5} />}
                            <TargetLabel>{target.id}</TargetLabel>
                            <TypeTag type={target.type}>{target.type}</TypeTag>
                        </TargetInfo>
                        <SelectBtn onClick={() => onTargetSelect(target.id)}>
                            <Crosshair size={14} />
                            Select
                        </SelectBtn>
                    </TargetItem>
                ))}
            </TargetList>
        </Root>
    );
};

export default TargetingPanel;
