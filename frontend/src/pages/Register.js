import React, { useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Link,
  Paper,
  CircularProgress,
  Grid,
} from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { toast } from 'react-toastify';
import axios from 'axios';

// API base URL - ajuste para a URL do seu backend
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Esquema de validação
const validationSchema = Yup.object({
  fullName: Yup.string()
    .required('Nome completo é obrigatório')
    .min(3, 'Nome deve ter pelo menos 3 caracteres'),
  email: Yup.string()
    .email('Email inválido')
    .required('Email é obrigatório'),
  password: Yup.string()
    .min(6, 'A senha deve ter pelo menos 6 caracteres')
    .required('Senha é obrigatória'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password'), null], 'As senhas devem ser iguais')
    .required('Confirmação de senha é obrigatória'),
  whatsappNumber: Yup.string()
    .matches(/^\+?[1-9]\d{10,14}$/, 'Número de WhatsApp inválido')
    .required('Número de WhatsApp é obrigatório'),
});

function Register() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: {
      fullName: '',
      email: '',
      password: '',
      confirmPassword: '',
      whatsappNumber: '',
    },
    validationSchema: validationSchema,
    onSubmit: async (values) => {
      setLoading(true);
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/register`, {
          full_name: values.fullName,
          email: values.email,
          password: values.password,
          whatsapp_number: values.whatsappNumber,
        });

        if (response.status === 201 || response.status === 200) {
          toast.success('Cadastro realizado com sucesso! Faça login para continuar.');
          navigate('/login');
        } else {
          throw new Error(response.data.message || 'Erro ao realizar cadastro');
        }
      } catch (error) {
        console.error('Erro ao registrar:', error);
        let errorMessage = 'Erro ao realizar cadastro';
        
        if (error.response) {
          // Erro da API
          errorMessage = error.response.data.message || errorMessage;
        } else if (error.request) {
          // Erro de conexão
          errorMessage = 'Não foi possível conectar ao servidor. Verifique sua conexão.';
        }
        
        toast.error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
  });

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper
          elevation={3}
          sx={{
            padding: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
          }}
        >
          <Typography component="h1" variant="h5" gutterBottom>
            WhatsApp Sales
          </Typography>
          <Typography component="h2" variant="h6" gutterBottom>
            Criar Conta
          </Typography>
          <Box
            component="form"
            onSubmit={formik.handleSubmit}
            sx={{ mt: 1, width: '100%' }}
          >
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="fullName"
                  label="Nome Completo"
                  name="fullName"
                  autoComplete="name"
                  value={formik.values.fullName}
                  onChange={formik.handleChange}
                  error={formik.touched.fullName && Boolean(formik.errors.fullName)}
                  helperText={formik.touched.fullName && formik.errors.fullName}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="email"
                  label="Email"
                  name="email"
                  autoComplete="email"
                  value={formik.values.email}
                  onChange={formik.handleChange}
                  error={formik.touched.email && Boolean(formik.errors.email)}
                  helperText={formik.touched.email && formik.errors.email}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="whatsappNumber"
                  label="Número do WhatsApp"
                  name="whatsappNumber"
                  placeholder="+5511999999999"
                  value={formik.values.whatsappNumber}
                  onChange={formik.handleChange}
                  error={formik.touched.whatsappNumber && Boolean(formik.errors.whatsappNumber)}
                  helperText={formik.touched.whatsappNumber && formik.errors.whatsappNumber}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="Senha"
                  type="password"
                  id="password"
                  autoComplete="new-password"
                  value={formik.values.password}
                  onChange={formik.handleChange}
                  error={formik.touched.password && Boolean(formik.errors.password)}
                  helperText={formik.touched.password && formik.errors.password}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="confirmPassword"
                  label="Confirmar Senha"
                  type="password"
                  id="confirmPassword"
                  value={formik.values.confirmPassword}
                  onChange={formik.handleChange}
                  error={formik.touched.confirmPassword && Boolean(formik.errors.confirmPassword)}
                  helperText={formik.touched.confirmPassword && formik.errors.confirmPassword}
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Cadastrar'}
            </Button>
            <Box sx={{ textAlign: 'center' }}>
              <Link component={RouterLink} to="/login" variant="body2">
                Já tem uma conta? Faça login
              </Link>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default Register; 