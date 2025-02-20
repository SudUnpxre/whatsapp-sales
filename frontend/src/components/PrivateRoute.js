import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

const PrivateRoute = ({ children }) => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const token = localStorage.getItem('token');

  // Verifica se o usuário está autenticado
  if (!isAuthenticated && !token) {
    // Redireciona para a página de login
    return <Navigate to="/login" replace />;
  }

  // Renderiza o componente filho se estiver autenticado
  return children;
};

export default PrivateRoute; 