import PropTypes from 'prop-types';

export const PlusSignButton = ({ onTap }) => {
    return (
        <button  className="fixed bottom-20 right-5 w-15 h-15 rounded-full bg-orange-200 text-black flex justify-center items-center text-2xl shadow-md hover:bg-blue-600 focus:outline-none"
            onClick={onTap}
            aria-label="Add"
        >
            +
        </button>
    );
};

PlusSignButton.propTypes = {
    onTap: PropTypes.func.isRequired,
};

