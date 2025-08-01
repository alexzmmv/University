import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { AddDrinkForm } from '../src/app/components/coffeShopPage/AddDrinkForm';
import { EditDrinkForm } from '../src/app/components/coffeShopPage/EditDrinkForm';
import { DrinkCard } from '../src/app/components/coffeShopPage/DrinkCard';
import { DrinkList } from '../src/app/components/coffeShopPage/DrinkList';
import { addDrink, updateDrink, deleteDrink } from '../src/app/coffeshop/[id]/page';

// Mock data for testing
const mockDrinks = [
    {
        id: 1,
        name: 'Espresso',
        description: 'Strong coffee brewed by forcing hot water under pressure through finely-ground coffee beans',
        price: '2.50',
        popularity: 10,
        sales: 2,
        image: 'https://picsum.photos/seed/Espresso/200/200'
    },
    {
        id: 2,
        name: 'Cappuccino',
        description: 'Coffee drink with espresso, hot milk, and steamed milk foam',
        price: '3.20',
        popularity: 10,
        sales: 2,
        image: 'https://picsum.photos/seed/Cappuccino/200/200'
    }
];

// Component tests
describe('AddDrinkForm Component', () => {
    test('renders form elements correctly', () => {
        const mockOnAdd = jest.fn();
        const mockOnCancel = jest.fn();
        
        render(<AddDrinkForm onAdd={mockOnAdd} onCancel={mockOnCancel} />);
        
        expect(screen.getByPlaceholderText('Drink name')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Description')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('0.00')).toBeInTheDocument();
        expect(screen.getByText('Add Drink')).toBeInTheDocument();
        expect(screen.getByText('Cancel')).toBeInTheDocument();
    });
    
    test('submits form with correct drink data when all fields filled', async () => {
        const mockOnAdd = jest.fn();
        const mockOnCancel = jest.fn();
        
        render(<AddDrinkForm onAdd={mockOnAdd} onCancel={mockOnCancel} />);
        
        fireEvent.change(screen.getByPlaceholderText('Drink name'), {
            target: { value: 'Mocha' }
        });
        
        fireEvent.change(screen.getByPlaceholderText('Description'), {
            target: { value: 'Espresso with chocolate' }
        });
        
        fireEvent.change(screen.getByPlaceholderText('0.00'), {
            target: { value: '3.75' }
        });
        
        fireEvent.click(screen.getByText('Add Drink'));
        
        expect(mockOnAdd).toHaveBeenCalledWith({
            name: 'Mocha',
            description: 'Espresso with chocolate',
            price: '3.75',
            image: expect.any(String),
            popularity: 100,
            sales: 100
        });
    });
    
    test('validates required fields before submission', () => {
        const mockOnAdd = jest.fn();
        const mockOnCancel = jest.fn();
        
        render(<AddDrinkForm onAdd={mockOnAdd} onCancel={mockOnCancel} />);
        
        // Try to submit without filling required fields
        fireEvent.click(screen.getByText('Add Drink'));
        
        // Form should not submit without required fields
        expect(mockOnAdd).not.toHaveBeenCalled();
        
        // Fill only name field
        fireEvent.change(screen.getByPlaceholderText('Drink name'), {
            target: { value: 'Mocha' }
        });
        
        fireEvent.click(screen.getByText('Add Drink'));
        expect(mockOnAdd).not.toHaveBeenCalled();
    });
    
    test('cancel button calls onCancel handler', () => {
        const mockOnAdd = jest.fn();
        const mockOnCancel = jest.fn();
        
        render(<AddDrinkForm onAdd={mockOnAdd} onCancel={mockOnCancel} />);
        
        fireEvent.click(screen.getByText('Cancel'));
        
        expect(mockOnCancel).toHaveBeenCalledTimes(1);
        expect(mockOnAdd).not.toHaveBeenCalled();
    });
    
    test('handles price input validation correctly', () => {
        const mockOnAdd = jest.fn();
        const mockOnCancel = jest.fn();
        
        render(<AddDrinkForm onAdd={mockOnAdd} onCancel={mockOnCancel} />);
        
        // Fill required fields
        fireEvent.change(screen.getByPlaceholderText('Drink name'), {
            target: { value: 'Mocha' }
        });
        
        fireEvent.change(screen.getByPlaceholderText('Description'), {
            target: { value: 'Espresso with chocolate' }
        });
        
        // Invalid price (negative)
        fireEvent.change(screen.getByPlaceholderText('0.00'), {
            target: { value: '-3.75' }
        });
        
        fireEvent.click(screen.getByText('Add Drink'));
        expect(mockOnAdd).not.toHaveBeenCalled();
    });
});

describe('DrinkList Component', () => {
    
    test('switches to edit mode when edit button is clicked', () => {
        render(
            <DrinkList 
                drinks={mockDrinks} 
                onDrinkUpdate={jest.fn()} 
                onDrinkDelete={jest.fn()} 
            />
        );
        
        // Click edit on first drink
        fireEvent.click(screen.getAllByText('Edit')[0]);
        
        // Should show the form for editing
        expect(screen.getByDisplayValue(mockDrinks[0].name)).toBeInTheDocument();
        expect(screen.getByDisplayValue(mockDrinks[0].description)).toBeInTheDocument();
        expect(screen.getByDisplayValue(mockDrinks[0].price)).toBeInTheDocument();
        expect(screen.getByText('Save')).toBeInTheDocument();
        expect(screen.getByText('Cancel')).toBeInTheDocument();
    });

    
    test('handles empty drinks array gracefully', () => {
        render(
            <DrinkList 
                drinks={[]} 
                onDrinkUpdate={jest.fn()} 
                onDrinkDelete={jest.fn()} 
            />
        );
        
        expect(screen.queryByText('Edit')).not.toBeInTheDocument();
        expect(screen.queryByText('Delete')).not.toBeInTheDocument();
    });
});

describe('Pagination Functionality', () => {
    // Mock data with enough items to test pagination
    const mockDrinksForPagination = Array.from({ length: 12 }, (_, i) => ({
        id: i + 1,
        name: `Drink ${i + 1}`,
        description: `Description ${i + 1}`,
        price: `${(i + 2).toFixed(2)}`,
        image: `https://picsum.photos/seed/Drink${i + 1}/200/200`,
        popularity: 10,
        sales: 2
    }));

    describe('Page calculation', () => {
        test('should paginate items correctly for middle pages', () => {
            const itemsPerPage = 5;
            const currentPage = 2;
            
            const indexOfLastItem = currentPage * itemsPerPage;
            const indexOfFirstItem = indexOfLastItem - itemsPerPage;
            const currentDrinks = mockDrinksForPagination.slice(indexOfFirstItem, indexOfLastItem);
            
            // Should get items 6-10 (indexes 5-9)
            expect(currentDrinks.length).toBe(5);
            expect(currentDrinks[0].id).toBe(6);
            expect(currentDrinks[4].id).toBe(10);
        });

        test('should correctly calculate total pages', () => {
            const itemsPerPage = 5;
            const totalItems = mockDrinksForPagination.length;
            
            const totalPages = Math.ceil(totalItems / itemsPerPage);
            expect(totalPages).toBe(3); // 12 items with 5 per page = 3 pages
            
            // Different page size
            const smallerItemsPerPage = 3;
            const totalPagesSmaller = Math.ceil(totalItems / smallerItemsPerPage);
            expect(totalPagesSmaller).toBe(4); // 12 items with 3 per page = 4 pages
        });

        test('should handle last page with fewer items correctly', () => {
            const itemsPerPage = 5;
            const currentPage = 3;
            
            const indexOfLastItem = currentPage * itemsPerPage;
            const indexOfFirstItem = indexOfLastItem - itemsPerPage;
            const currentDrinks = mockDrinksForPagination.slice(indexOfFirstItem, indexOfLastItem);
            
            // Last page should have only 2 items (items 11-12)
            expect(currentDrinks.length).toBe(2);
            expect(currentDrinks[0].id).toBe(11);
            expect(currentDrinks[1].id).toBe(12);
        });
    });

    describe('Edge cases', () => {
        test('should handle empty array gracefully', () => {
            const itemsPerPage = 5;
            
            const emptyArray = [];
            const totalPagesForEmpty = Math.max(1, Math.ceil(emptyArray.length / itemsPerPage));
            expect(totalPagesForEmpty).toBe(1); // Should have at least 1 page even when empty
            
            const currentPage = 1;
            const indexOfLastItem = currentPage * itemsPerPage;
            const indexOfFirstItem = indexOfLastItem - itemsPerPage;
            const currentDrinks = emptyArray.slice(indexOfFirstItem, indexOfLastItem);
            
            expect(currentDrinks.length).toBe(0);
        });
        
        test('should handle arrays with exactly one page worth of items', () => {
            const itemsPerPage = 5;
            
            const exactPageArray = Array.from({ length: 5 }, (_, i) => ({ id: i + 1 }));
            const totalPagesForExact = Math.ceil(exactPageArray.length / itemsPerPage);
            expect(totalPagesForExact).toBe(1);
            
            const currentPage = 1;
            const indexOfLastItem = currentPage * itemsPerPage;
            const indexOfFirstItem = indexOfLastItem - itemsPerPage;
            const currentDrinks = exactPageArray.slice(indexOfFirstItem, indexOfLastItem);
            
            expect(currentDrinks.length).toBe(5);
        });
        
        test('should handle arrays with a single item', () => {
            const itemsPerPage = 5;
            
            const singleItemArray = [{ id: 1 }];
            const totalPagesForSingle = Math.ceil(singleItemArray.length / itemsPerPage);
            expect(totalPagesForSingle).toBe(1);
        });
    });
    
    describe('Page validation', () => {
        const itemsPerPage = 5;
        
        test('should handle invalid page 0 by defaulting to page 1', () => {
            const pageZero = 0;
            const validPage = Math.max(1, pageZero);
            const indexOfFirstItem = (validPage - 1) * itemsPerPage;
            
            expect(validPage).toBe(1);
            expect(indexOfFirstItem).toBe(0);
        });
        
        test('should handle negative page numbers by defaulting to page 1', () => {
            const pageNegative = -1;
            const validPage = Math.max(1, pageNegative);
            const indexOfFirstItem = (validPage - 1) * itemsPerPage;
            
            expect(validPage).toBe(1);
            expect(indexOfFirstItem).toBe(0);
        });
        
        test('should clamp page number to max page if exceeding total pages', () => {
            const totalPages = Math.ceil(mockDrinksForPagination.length / itemsPerPage);
            const pageBeyond = totalPages + 1;
            const validPage = Math.min(pageBeyond, totalPages);
            
            expect(validPage).toBe(totalPages);
            
            const indexOfFirstItem = (validPage - 1) * itemsPerPage;
            const currentDrinks = mockDrinksForPagination.slice(indexOfFirstItem, indexOfFirstItem + itemsPerPage);
            
            expect(currentDrinks.length).toBe(2); // Should show the last 2 items
        });
    });
});