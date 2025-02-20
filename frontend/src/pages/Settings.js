import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Switch,
  FormControlLabel,
  Divider,
  Alert,
  Snackbar,
  Card,
  CardContent,
  CardHeader,
  CircularProgress,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
} from '@mui/material';
import { useFormik } from 'formik';
import * as Yup from 'yup';

// Esquema de validação para as configurações
const settingsValidationSchema = Yup.object({
  whatsappNumber: Yup.string()
    .matches(/^\+?[1-9]\d{10,14}$/, 'Número de WhatsApp inválido')
    .required('Número de WhatsApp é obrigatório'),
  businessName: Yup.string()
    .required('Nome do negócio é obrigatório')
    .min(3, 'Nome deve ter pelo menos 3 caracteres'),
  email: Yup.string()
    .email('Email inválido')
    .required('Email é obrigatório'),
  plan: Yup.string()
    .required('Plano é obrigatório'),
  autoReply: Yup.boolean(),
  autoReplyMessage: Yup.string()
    .when('autoReply', {
      is: true,
      then: Yup.string().required('Mensagem automática é obrigatória'),
    }),
  followUpEnabled: Yup.boolean(),
  followUpDelay: Yup.number()
    .when('followUpEnabled', {
      is: true,
      then: Yup.number()
        .required('Tempo de espera é obrigatório')
        .min(1, 'Tempo mínimo é 1 hora')
        .max(72, 'Tempo máximo é 72 horas'),
    }),
});

function Settings() {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.auth.user);
  const loading = useSelector((state) => state.auth.loading);
  const [success, setSuccess] = useState(false);

  const formik = useFormik({
    initialValues: {
      whatsappNumber: user?.whatsapp_number || '',
      businessName: user?.business_name || '',
      email: user?.email || '',
      plan: user?.plan_type || 'free',
      autoReply: false,
      autoReplyMessage: '',
      followUpEnabled: false,
      followUpDelay: 24,
    },
    validationSchema: settingsValidationSchema,
    onSubmit: async (values) => {
      try {
        // Aqui você deve implementar a lógica para salvar as configurações
        // await dispatch(updateSettings(values));
        setSuccess(true);
      } catch (error) {
        console.error('Erro ao salvar configurações:', error);
      }
    },
  });

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom component="div">
        Configurações
      </Typography>

      <Grid container spacing={3}>
        {/* Configurações do Perfil */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Perfil" />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    name="businessName"
                    label="Nome do Negócio"
                    value={formik.values.businessName}
                    onChange={formik.handleChange}
                    error={formik.touched.businessName && Boolean(formik.errors.businessName)}
                    helperText={formik.touched.businessName && formik.errors.businessName}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    name="email"
                    label="Email"
                    value={formik.values.email}
                    onChange={formik.handleChange}
                    error={formik.touched.email && Boolean(formik.errors.email)}
                    helperText={formik.touched.email && formik.errors.email}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    name="whatsappNumber"
                    label="Número do WhatsApp"
                    value={formik.values.whatsappNumber}
                    onChange={formik.handleChange}
                    error={formik.touched.whatsappNumber && Boolean(formik.errors.whatsappNumber)}
                    helperText={formik.touched.whatsappNumber && formik.errors.whatsappNumber}
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Configurações do Plano */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Plano" />
            <CardContent>
              <FormControl fullWidth>
                <InputLabel>Plano Atual</InputLabel>
                <Select
                  name="plan"
                  value={formik.values.plan}
                  label="Plano Atual"
                  onChange={formik.handleChange}
                >
                  <MenuItem value="free">Gratuito</MenuItem>
                  <MenuItem value="premium">Premium</MenuItem>
                  <MenuItem value="enterprise">Enterprise</MenuItem>
                </Select>
              </FormControl>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  {formik.values.plan === 'free' && '50 mensagens/mês'}
                  {formik.values.plan === 'premium' && 'Mensagens ilimitadas'}
                  {formik.values.plan === 'enterprise' && 'Recursos personalizados'}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Configurações de Automação */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="Automação" />
            <CardContent>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        name="autoReply"
                        checked={formik.values.autoReply}
                        onChange={formik.handleChange}
                      />
                    }
                    label="Resposta Automática"
                  />
                </Grid>
                {formik.values.autoReply && (
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      multiline
                      rows={3}
                      name="autoReplyMessage"
                      label="Mensagem de Resposta Automática"
                      value={formik.values.autoReplyMessage}
                      onChange={formik.handleChange}
                      error={formik.touched.autoReplyMessage && Boolean(formik.errors.autoReplyMessage)}
                      helperText={formik.touched.autoReplyMessage && formik.errors.autoReplyMessage}
                    />
                  </Grid>
                )}
                <Grid item xs={12}>
                  <Divider />
                </Grid>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        name="followUpEnabled"
                        checked={formik.values.followUpEnabled}
                        onChange={formik.handleChange}
                      />
                    }
                    label="Follow-up Automático"
                  />
                </Grid>
                {formik.values.followUpEnabled && (
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      type="number"
                      name="followUpDelay"
                      label="Tempo de Espera (horas)"
                      value={formik.values.followUpDelay}
                      onChange={formik.handleChange}
                      error={formik.touched.followUpDelay && Boolean(formik.errors.followUpDelay)}
                      helperText={formik.touched.followUpDelay && formik.errors.followUpDelay}
                    />
                  </Grid>
                )}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          onClick={formik.handleSubmit}
          disabled={!formik.isValid || formik.isSubmitting}
        >
          Salvar Configurações
        </Button>
      </Box>

      <Snackbar
        open={success}
        autoHideDuration={6000}
        onClose={() => setSuccess(false)}
      >
        <Alert severity="success" sx={{ width: '100%' }}>
          Configurações salvas com sucesso!
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default Settings; 