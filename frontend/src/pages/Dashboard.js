import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CircularProgress,
} from '@mui/material';
import {
  WhatsApp as WhatsAppIcon,
  ShoppingCart as OrderIcon,
  People as CustomerIcon,
  AttachMoney as RevenueIcon,
} from '@mui/icons-material';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Registra os componentes necessários do Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Dashboard() {
  const dispatch = useDispatch();
  const { statistics: orderStats } = useSelector((state) => state.orders);
  const { statistics: customerStats } = useSelector((state) => state.customers);
  const loading = useSelector((state) => state.orders.loading || state.customers.loading);

  useEffect(() => {
    // Aqui você deve implementar a lógica para carregar as estatísticas
    // dispatch(fetchOrderStatistics());
    // dispatch(fetchCustomerStatistics());
  }, [dispatch]);

  // Dados para o gráfico de receita
  const revenueData = {
    labels: orderStats.revenueByDay?.map(day => day.date) || [],
    datasets: [
      {
        label: 'Receita Diária',
        data: orderStats.revenueByDay?.map(day => day.revenue) || [],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  // Dados para o gráfico de pedidos por status
  const orderStatusData = {
    labels: Object.keys(orderStats.ordersByStatus || {}),
    datasets: [
      {
        label: 'Pedidos por Status',
        data: Object.values(orderStats.ordersByStatus || {}),
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
        ],
      },
    ],
  };

  const StatCard = ({ title, value, icon, color }) => (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          {React.cloneElement(icon, { sx: { color, mr: 1 } })}
          <Typography color="textSecondary" variant="h6">
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" component="div">
          {value}
        </Typography>
      </CardContent>
    </Card>
  );

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
        Dashboard
      </Typography>

      {/* Cards de Estatísticas */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total de Pedidos"
            value={orderStats.totalOrders || 0}
            icon={<OrderIcon />}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Receita Total"
            value={`R$ ${orderStats.totalRevenue?.toFixed(2) || '0.00'}`}
            icon={<RevenueIcon />}
            color="#2e7d32"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total de Clientes"
            value={customerStats.totalCustomers || 0}
            icon={<CustomerIcon />}
            color="#ed6c02"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Clientes Ativos"
            value={customerStats.activeCustomers || 0}
            icon={<WhatsAppIcon />}
            color="#25D366"
          />
        </Grid>
      </Grid>

      {/* Gráficos */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Receita Diária
            </Typography>
            <Box sx={{ height: 300 }}>
              <Line
                data={revenueData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                    y: {
                      beginAtZero: true,
                    },
                  },
                }}
              />
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Pedidos por Status
            </Typography>
            <Box sx={{ height: 300 }}>
              <Bar
                data={orderStatusData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                    y: {
                      beginAtZero: true,
                    },
                  },
                }}
              />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard; 