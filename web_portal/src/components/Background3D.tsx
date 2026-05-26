import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Points, PointMaterial } from '@react-three/drei';
import * as THREE from 'three';

const NeuralNodes = () => {
  const pointsRef = useRef<THREE.Points>(null);
  
  const particleCount = 200;
  
  const [positions, mathColors] = useMemo(() => {
    const p = new Float32Array(particleCount * 3);
    const c = new Float32Array(particleCount * 3);
    
    for (let i = 0; i < particleCount; i++) {
      p[i * 3] = (Math.random() - 0.5) * 20;
      p[i * 3 + 1] = (Math.random() - 0.5) * 20;
      p[i * 3 + 2] = (Math.random() - 0.5) * 20;
      
      const color = new THREE.Color();
      // Cyberpunk cyan to neon blue
      color.setHSL(0.5 + Math.random() * 0.1, 1.0, 0.5);
      c[i * 3] = color.r;
      c[i * 3 + 1] = color.g;
      c[i * 3 + 2] = color.b;
    }
    
    return [p, c];
  }, []);

  useFrame((state, delta) => {
    if (pointsRef.current) {
      pointsRef.current.rotation.x -= delta / 10;
      pointsRef.current.rotation.y -= delta / 15;
    }
  });

  return (
    <Points ref={pointsRef} positions={positions} colors={mathColors} stride={3} frustumCulled={false}>
      <PointMaterial
        transparent
        vertexColors
        size={0.15}
        sizeAttenuation={true}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </Points>
  );
};

export const Background3D: React.FC = () => {
  return (
    <div className="fixed inset-0 z-[-1] bg-black">
      <Canvas camera={{ position: [0, 0, 10], fov: 60 }}>
        <ambientLight intensity={0.5} />
        <NeuralNodes />
      </Canvas>
    </div>
  );
};
