import React from 'react';
import styled, { keyframes } from 'styled-components';
import { Cpu, Zap, Activity } from 'lucide-react';

const flow = keyframes`
  0% { stroke-dashoffset: 200; }
  100% { stroke-dashoffset: 0; }
`;

const Root = styled.div`
    height: 100%;
    width: 100%;
    position: relative;
`;

const Node = styled.div`
    position: absolute;
    background: ${props => props.theme.colors.bg};
    color: ${props => props.theme.colors.text};
    border: 1px solid ${props => props.theme.colors.border};
    border-radius: 15px;
    padding: 12px 18px;
    font-size: 0.8rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: ${props => props.theme.effects.shadow};
    left: ${props => props.x}px;
    top: ${props => props.y}px;
    transform: translate(-50%, -50%);
`;

const SvgCanvas = styled.svg`
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
`;

const Path = styled.path`
    fill: none;
    stroke: ${props => props.theme.colors.primary}44;
    stroke-width: 2;
`;

const AnimatedPath = styled.path`
    fill: none;
    stroke: ${props => props.theme.colors.primary};
    stroke-width: 2;
    stroke-dasharray: 10, 10;
    animation: ${flow} 2s linear infinite;
`;

const NeuralPathwayHUD = () => {
    const nodes = {
        input: { x: 50, y: 150, label: 'INPUT', icon: <Zap /> },
        jarvis: { x: 200, y: 150, label: 'JARVIS CORE', icon: <Cpu /> },
        brain: { x: 350, y: 80, label: 'BRAINBRIDGE', icon: <Activity /> },
        shadow: { x: 350, y: 220, label: 'SHADOW_AI', icon: <Activity /> },
    };

    const getPathD = (from, to) => {
        return `M ${from.x},${from.y} C ${from.x + 80},${from.y} ${to.x - 80},${to.y} ${to.x},${to.y}`;
    };

    return (
        <Root>
            <SvgCanvas>
                <Path d={getPathD(nodes.input, nodes.jarvis)} />
                <AnimatedPath d={getPathD(nodes.input, nodes.jarvis)} />
                
                <Path d={getPathD(nodes.jarvis, nodes.brain)} />
                <AnimatedPath d={getPathD(nodes.jarvis, nodes.brain)} />

                <Path d={getPathD(nodes.jarvis, nodes.shadow)} />
            </SvgCanvas>
            {Object.values(nodes).map(node => (
                <Node key={node.label} x={node.x} y={node.y}>
                    {node.icon} {node.label}
                </Node>
            ))}
        </Root>
    );
};

export default NeuralPathwayHUD;
