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
  Chip,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  MenuItem,
  Grid,
  CircularProgress,
} from '@mui/material';
import {
  Visibility as ViewIcon,
  Edit as EditIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

// Componente de Status do Pedido
const OrderStatus = ({ status }) => {
  const statusConfig = {
    pending: { label: 'Pendente', color: 'warning' },
    paid: { label: 'Pago', color: 'success' },
    cancelled: { label: 'Cancelado', color: 'error' },
    delivered: { label: 'Entregue', color: 'info' },
  };

  const config = statusConfig[status] || { label: status, color: 'default' };

  return <Chip label={config.label} color={config.color} size="small" />;
};

function Orders() {
  const dispatch = useDispatch();
  const orders = useSelector((state) => state.orders.orders);
  const loading = useSelector((state) => state.orders.loading);
  const pagination = useSelector((state) => state.orders.pagination);

  const [selectedOrder, setSelectedOrder] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    // Aqui você deve implementar a lógica para carregar os pedidos
    // dispatch(fetchOrders());
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

  const handleViewOrder = (order) => {
    setSelectedOrder(order);
    setEditMode(false);
    setOpenDialog(true);
  };

  const handleEditOrder = (order) => {
    setSelectedOrder(order);
    setEditMode(true);
    setOpenDialog(true);
  };

  const handleCancelOrder = (orderId) => {
    if (window.confirm('Tem certeza que deseja cancelar este pedido?')) {
      // dispatch(cancelOrder(orderId));
    }
  };

  const handleCloseDialog = () => {
    setSelectedOrder(null);
    setEditMode(false);
    setOpenDialog(false);
  };

  const handleUpdateOrder = () => {
    // Implementar lógica de atualização do pedido
    handleCloseDialog();
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
        Pedidos
      </Typography>

      <Paper sx={{ width: '100%', mb: 2 }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Cliente</TableCell>
                <TableCell>Data</TableCell>
                <TableCell>Total</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Pagamento</TableCell>
                <TableCell align="right">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {orders.map((order) => (
                <TableRow key={order.id}>
                  <TableCell>#{order.id}</TableCell>
                  <TableCell>{order.customer.name}</TableCell>
                  <TableCell>
                    {format(new Date(order.created_at), 'dd/MM/yyyy HH:mm', {
                      locale: ptBR,
                    })}
                  </TableCell>
                  <TableCell>R$ {order.total_amount.toFixed(2)}</TableCell>
                  <TableCell>
                    <OrderStatus status={order.status} />
                  </TableCell>
                  <TableCell>{order.payment_method}</TableCell>
                  <TableCell align="right">
                    <IconButton
                      color="primary"
                      onClick={() => handleViewOrder(order)}
                    >
                      <ViewIcon />
                    </IconButton>
                    <IconButton
                      color="info"
                      onClick={() => handleEditOrder(order)}
                      disabled={order.status === 'cancelled'}
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      color="error"
                      onClick={() => handleCancelOrder(order.id)}
                      disabled={
                        order.status === 'cancelled' || order.status === 'delivered'
                      }
                    >
                      <CancelIcon />
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

      {/* Dialog de Detalhes/Edição do Pedido */}
      <Dialog
        open={openDialog}
        onClose={handleCloseDialog}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {editMode ? 'Editar Pedido' : 'Detalhes do Pedido'} #{selectedOrder?.id}
        </DialogTitle>
        <DialogContent>
          {selectedOrder && (
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Cliente"
                  value={selectedOrder.customer.name}
                  disabled
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="WhatsApp"
                  value={selectedOrder.customer.whatsapp_number}
                  disabled
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Data do Pedido"
                  value={format(
                    new Date(selectedOrder.created_at),
                    'dd/MM/yyyy HH:mm',
                    { locale: ptBR }
                  )}
                  disabled
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  select
                  label="Status"
                  value={selectedOrder.status}
                  disabled={!editMode}
                  onChange={(e) =>
                    setSelectedOrder({
                      ...selectedOrder,
                      status: e.target.value,
                    })
                  }
                >
                  <MenuItem value="pending">Pendente</MenuItem>
                  <MenuItem value="paid">Pago</MenuItem>
                  <MenuItem value="delivered">Entregue</MenuItem>
                  <MenuItem value="cancelled">Cancelado</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Itens do Pedido
                </Typography>
                <TableContainer component={Paper}>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Produto</TableCell>
                        <TableCell align="right">Quantidade</TableCell>
                        <TableCell align="right">Preço Unit.</TableCell>
                        <TableCell align="right">Total</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {selectedOrder.items.map((item) => (
                        <TableRow key={item.id}>
                          <TableCell>{item.product.name}</TableCell>
                          <TableCell align="right">{item.quantity}</TableCell>
                          <TableCell align="right">
                            R$ {item.unit_price.toFixed(2)}
                          </TableCell>
                          <TableCell align="right">
                            R$ {(item.quantity * item.unit_price).toFixed(2)}
                          </TableCell>
                        </TableRow>
                      ))}
                      <TableRow>
                        <TableCell colSpan={3} align="right">
                          <strong>Total</strong>
                        </TableCell>
                        <TableCell align="right">
                          <strong>
                            R$ {selectedOrder.total_amount.toFixed(2)}
                          </strong>
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Fechar</Button>
          {editMode && (
            <Button onClick={handleUpdateOrder} variant="contained">
              Salvar Alterações
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Orders; 