# Frontend Performance & UI Smoothness

This document outlines the extreme performance optimizations required to maintain 60FPS in a high-frequency trading dashboard.

## The 16.6ms Budget

To maintain a smooth 60 frames per second, the main thread must process all React reconciliation, state updates, and layout calculations in under 16.6ms.

## React Rendering Optimization

Unnecessary re-renders are the primary cause of UI stutter. We strictly enforce shallow equality checks before allowing a component to update.

