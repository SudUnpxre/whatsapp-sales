import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  IconButton,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Grid,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Visibility as ViewIcon,
  WhatsApp as WhatsAppIcon,
  Send as SendIcon,
} from '@mui/icons-material';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

// Componente TabPanel para o diálogo de detalhes
function TabPanel({ children, value, index }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`customer-tabpanel-${index}`}
      aria-labelledby={`customer-tab-${index}`}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function Customers() {
  const dispatch = useDispatch();
  const customers = useSelector((state) => state.customers.customers);
  const loading = useSelector((state) => state.customers.loading);
  const pagination = useSelector((state) => state.customers.pagination);

  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Aqui você deve implementar a lógica para carregar os clientes
    // dispatch(fetchCustomers());
  }, [dispatch]);

  const handleChangePage = (event, newPage) => {
    // dispatch(setPagination({ ...pagination, page: newPage + 1 }));
  };

  const handleChangeRowsPerPage = (event) => {
    // dispatch(setPagination({
    //   ...pagination,
    //   limit: parseInt(event.target.value, 10),
    //   page: 1,
    // }));
  };

  const handleViewCustomer = (customer) => {
    setSelectedCustomer(customer);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setSelectedCustomer(null);
    setOpenDialog(false);
    setTabValue(0);
    setMessage('');
  };

  const handleSendMessage = () => {
    if (message.trim() && selectedCustomer) {
      // Aqui você deve implementar a lógica para enviar mensagem
      // dispatch(sendWhatsAppMessage({
      //   customerId: selectedCustomer.id,
      //   message: message.trim(),
      // }));
      setMessage('');
    }
  };

  const handleChangeTab = (event, newValue) => {
    setTabValue(newValue);
  };

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
        Clientes
      </Typography>

      <Paper sx={{ width: '100%', mb: 2 }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Nome</TableCell>
                <TableCell>WhatsApp</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Última Interação</TableCell>
                <TableCell>Total de Pedidos</TableCell>
                <TableCell align="right">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {customers.map((customer) => (
                <TableRow key={customer.id}>
                  <TableCell>{customer.name}</TableCell>
                  <TableCell>{customer.whatsapp_number}</TableCell>
                  <TableCell>{customer.email}</TableCell>
                  <TableCell>
                    {customer.last_interaction
                      ? format(new Date(customer.last_interaction), 'dd/MM/yyyy HH:mm', {
                          locale: ptBR,
                        })
                      : 'Nunca'}
                  </TableCell>
                  <TableCell>{customer.orders?.length || 0}</TableCell>
                  <TableCell align="right">
                    <IconButton
                      color="primary"
                      onClick={() => handleViewCustomer(customer)}
                    >
                      <ViewIcon />
                    </IconButton>
                    <IconButton
                      color="success"
                      href={`https://wa.me/${customer.whatsapp_number}`}
                      target="_blank"
                    >
                      <WhatsAppIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={pagination.total}
          rowsPerPage={pagination.limit}
          page={pagination.page - 1}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          labelRowsPerPage="Itens por página"
        />
      </Paper>

      {/* Dialog de Detalhes do Cliente */}
      <Dialog
        open={openDialog}
        onClose={handleCloseDialog}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Detalhes do Cliente</DialogTitle>
        <DialogContent>
          {selectedCustomer && (
            <Box sx={{ width: '100%' }}>
              <Tabs
                value={tabValue}
                onChange={handleChangeTab}
                aria-label="customer details tabs"
              >
                <Tab label="Informações" />
                <Tab label="Pedidos" />
                <Tab label="Interações" />
                <Tab label="Mensagem" />
              </Tabs>

              {/* Aba de Informações */}
              <TabPanel value={tabValue} index={0}>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Nome"
                      value={selectedCustomer.name}
                      disabled
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="WhatsApp"
                      value={selectedCustomer.whatsapp_number}
                      disabled
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Email"
                      value={selectedCustomer.email}
                      disabled
                    />
                  </Grid>
                </Grid>
              </TabPanel>

              {/* Aba de Pedidos */}
              <TabPanel value={tabValue} index={1}>
                <List>
                  {selectedCustomer.orders?.map((order) => (
                    <React.Fragment key={order.id}>
                      <ListItem>
                        <ListItemText
                          primary={`Pedido #${order.id}`}
                          secondary={`
                            Data: ${format(new Date(order.created_at), 'dd/MM/yyyy HH:mm', {
                              locale: ptBR,
                            })}
                            | Status: ${order.status}
                            | Total: R$ ${order.total_amount.toFixed(2)}
                          `}
                        />
                      </ListItem>
                      <Divider />
                    </React.Fragment>
                  ))}
                </List>
              </TabPanel>

              {/* Aba de Interações */}
              <TabPanel value={tabValue} index={2}>
                <List>
                  {selectedCustomer.interaction_history?.map((interaction, index) => (
                    <React.Fragment key={index}>
                      <ListItem>
                        <ListItemText
                          primary={format(
                            new Date(interaction.timestamp),
                            'dd/MM/yyyy HH:mm',
                            { locale: ptBR }
                          )}
                          secondary={interaction.content}
                        />
                      </ListItem>
                      <Divider />
                    </React.Fragment>
                  ))}
                </List>
              </TabPanel>

              {/* Aba de Mensagem */}
              <TabPanel value={tabValue} index={3}>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      multiline
                      rows={4}
                      label="Mensagem"
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      placeholder="Digite uma mensagem para enviar via WhatsApp..."
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <Button
                      fullWidth
                      variant="contained"
                      startIcon={<SendIcon />}
                      onClick={handleSendMessage}
                      disabled={!message.trim()}
                    >
                      Enviar Mensagem
                    </Button>
                  </Grid>
                </Grid>
              </TabPanel>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Fechar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Customers; 