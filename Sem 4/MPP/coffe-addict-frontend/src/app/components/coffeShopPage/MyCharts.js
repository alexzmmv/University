import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const SalesChart = ({ data }) => (
    <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="sales" stroke="#8884d8" />
        </LineChart>
    </ResponsiveContainer>
);

const RevenueChart = ({ data }) => (
    <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="revenue" stroke="#82ca9d" />
        </LineChart>
    </ResponsiveContainer>
);

const PopularityChart = ({ data }) => (
    <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="popularity" stroke="#ffc658" />
        </LineChart>
    </ResponsiveContainer>
);

export const MyCharts = ({ drinks }) => {
    return (
        <div className="hidden md:block w-full max-w-4xl mt-8">
            <h2 className="text-xl font-bold mb-4">Sales Data</h2>
            <SalesChart data={drinks.map(drink => ({ name: drink.name, sales: drink.sales || 0 }))} />
                    
            <h2 className="text-xl font-bold mt-8 mb-4">Revenue Data</h2>
            <RevenueChart data={drinks.map(drink => ({ 
                        name: drink.name, 
                        revenue: (drink.sales || 0) * parseFloat(drink.price || 0)
                    }))} />
                    
            <h2 className="text-xl font-bold mt-8 mb-4">Popularity Data</h2>
            <PopularityChart data={drinks.map(drink => ({ name: drink.name, popularity: drink.popularity || 0 }))} />
        </div>
    );
}